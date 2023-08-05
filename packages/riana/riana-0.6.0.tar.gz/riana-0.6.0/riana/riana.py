"""
Relative Isotope Abundance Analyzer v.0.6.0. Build Date : : :.
Written by Edward Lau (lau1@stanford.edu) 2016-2019


"""


from riana.read_directory import ReadDirectory
from riana.read_peptide import ReadPercolator
from riana.parse_mzml import Mzml
from riana.integrate_peaks import Peaks
import re
import os
import sys
import datetime
import tqdm
from multiprocessing import cpu_count
from riana import __version__
import logging


def runRiana(args):
    """
    Improved process to integrate for isotope abundance analysis.
    Idea is to loop through the mzML only once - get all the peptides to be integrated first
    Find all the spectrum ID - m/z combinations to be integrated, then integrate them sequentially

    :param args: Arguments from command line
    :return:

    """

    # Get timestamp for out files
    now = datetime.datetime.now()
    directory_to_write = os.path.join(args.out, 'riana_' + now.strftime('%Y%m%d%H%M%S'))
    os.makedirs(directory_to_write, exist_ok=True)

    main_log = logging.getLogger('riana')
    main_log.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(os.path.join(directory_to_write, 'riana.log'))
    fh.setLevel(logging.INFO)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    main_log.addHandler(fh)
    main_log.addHandler(ch)

    main_log.info(args)
    main_log.info(__version__)

    # Handle command line arguments
    unique_pep = args.unique

    lysine_filter = args.lysine  # Does lysine peptides only (for Liverpool aa labeling data
    try:
        lysine_filter = int(lysine_filter)
        if lysine_filter not in [1, 2, 3]:
            lysine_filter = 0

    except TypeError or ValueError:
        lysine_filter = 0

    #
    # Convert the to-do isotopomer list option into a list of integers
    #
    iso_to_do = []

    for char in args.iso.split(','):

        try:
            char = int(char)

            # Only doing down to mz + 12.
            if char <= 12:
                iso_to_do.append(int(char))

        except ValueError or TypeError:
            pass

    if not iso_to_do:
        sys.exit('Error: Invalid isotopomer list given.')

    iso_to_do = list(set(iso_to_do))
    iso_to_do.sort()


    #
    # Percolator q value cutoff for peptides and proteins
    #
    if args.qvalue:

        try:
            qcutoff = float(args.qvalue)

        except ValueError or TypeError:
            print('Invalid Q value given - using default value.')
            qcutoff = float(1e-2)

    #
    # Retention time cutoff peptides and proteins
    #
    if args.rtime:

        try:
            rt_tolerance = float(args.rtime)

        except ValueError or TypeError:
            print('Invalid retention time tolerance given - using default value.')
            rt_tolerance = float(1.0)
    else:
        rt_tolerance = float(1.0)

    #
    # MS1 mass tolerance for integration
    #
    if args.masstolerance:
        try:
            mass_tolerance = float(args.masstolerance) * 1e-6

        except ValueError or TypeError:
            print('Invalid mass tolerance given - using default value.')
            mass_tolerance = float(100) * 1e-6
    else:
        mass_tolerance = float(100) * 1e-6

    #
    # Multi-threading
    #
    if args.thread:
        try:
            num_thread = max(cpu_count()-1, int(args.thread))

        except ValueError or TypeError:
            print('Invalid thread count, using default.')
            num_thread = 4
    else:
        num_thread = 4

    #
    # Inclusion lists
    #
    if args.amrt:
        input_type = 'AMRT'  #"lipid"
    else:
        input_type = 'Percolator'

    dir_loc = args.dir
    assert os.path.isdir(dir_loc), '[error] project directory not valid'

    # This is the directory that holds the entire project
    project = ReadDirectory(dir_loc)

    # Get the master peptide ID list
    if input_type == 'Percolator':
        mzid = ReadPercolator(project, directory_to_write)
        mzid.read_all_project_psms()
        mzid.make_master_match_list(lysine_filter=lysine_filter,
                                    peptide_q=qcutoff,
                                    unique_only=unique_pep,)

    elif input_type == 'AMRT':
        raise Exception('AMRT temporarily not supported while we work on Match Between Runs')
        sys.exit()

    # 2020-02-27 Need to rewrite ReadLipid module to be like ReadPercolator (reading all IDs in project at once)
    '''
    elif mol_type == 'lipid':
    # Get a master lipid id list
        for sample in tqdm.tqdm(samples, desc='Processing Sample'):

            sample_loc = os.path.join(project.path, sample)
            try:
                mzid = ReadLipid(sample_loc)
                #mzid.get_mzid_indices()

            except OSError as e:
                sys.exit('Failed to load am_rt file. ' + str(e.errno))
    '''

    # Each subdirectory is a sample
    samples = project.samples

    for current_sample in tqdm.tqdm(samples, desc='Processing Sample', total=len(samples)):

        sample_loc = os.path.join(project.path, current_sample)

        #
        # Open the mzid file
        # Note 2018-09-07 - I am not sure we should use the Mzid module anymore since Percolator doesn't seem to output
        # Mzid files that conform completely to Mzid standards. In particular I wasn't able to locate where in the xml file
        # is the file_idx (mzml file from which the spectrum was found) is encoded. It would be much easier at this point to use
        # the percolator tab-delimited file. Unless I can look at a multi-fraction Percolator run Mzid and modify the Mzid module from there
        #
        """
        try:
            mzid = Mzid(mzid_loc)
            mzid.make_peptide_summary(take_psm_df_cvParams=False)
            mzid.filter_peptide_summary(lysine_filter=lysine_filter,
                                        protein_q=qcutoff,
                                        peptide_q=1,
                                        unique_only=unique_pep,
                                        require_protein_id=True)
    
        except OSError as e:
            sys.exit('Failed to load mzid file. ' + str(e.errno))
        """

        mzid.get_current_sample_psms(current_sample=current_sample)
        mzid.get_current_sample_mzid_indices()

        mzml_files = [f for f in os.listdir(sample_loc) if re.match('^.*.mzML', f)]

        # Sort the mzML files by names
        # Note this may create a problem if the OS Percolator runs on has natural sorting (xxxx_2 before xxxx_10)
        # But we will ignore for now
        mzml_files.sort()

        # Throw an error if there is no mzML file in the mzml directory
        assert len(mzml_files) != 0, '[error] no mzml files in the specified directory'
        # Check that the number of mzMLs in the mzML folder is the same as the maximum of the ID file's file_idx column.
        # Note this will break if the last fraction does not contain at least some ID, but we will ignore for now.
        assert len(mzml_files) == max(mzid.indices) + 1, '[error] number of mzml files not matching id list'

        #
        # Read the mzml files
        #

        # For each file index (fraction), open the mzML file, and create a subset Percolator ID dataframe
        for idx in mzid.indices:

            # Verbosity 0 progress message
            main_log.info('Doing mzml: {0} ({1} of {2})'.format(
                mzml_files[idx],
                str(idx + 1),
                str(len(mzid.indices))))

            # Make a subset dataframe with the current file index (fraction) being considered
            mzid.get_current_fraction_psms(idx)
            mzid.filter_current_fraction_psms(lysine_filter=lysine_filter,
                                              protein_q=1,
                                              peptide_q=qcutoff,
                                              unique_only=unique_pep,
                                              use_soft_threshold=True,
                                              match_across_runs=True)

            try:
                mzml = Mzml(os.path.join(sample_loc, mzml_files[idx]))
            except OSError as e:
                sys.exit('[error] failed to load fraction mzml file. ' + str(e.errno))

            #
            # Read the spectra into dictionary and also create MS1/MS2 indices as a Peaks object
            #
            mzml.parse_mzml()
            peaks = Peaks(msdata=mzml.msdata,
                          rt_idx=mzml.rt_idx,
                          mslvl_idx=mzml.mslvl_idx,
                          input_type=input_type,
                          directory_to_write=directory_to_write)

            #
            # Link ID file, iso_to_do, and rt_tolerance to mzML
            #
            peaks.associate_id(mzid.curr_frac_filtered_id_df)
            peaks.set_iso_to_do(iso_to_do)
            peaks.set_rt_tolerance(rt_tolerance)
            peaks.set_mass_tolerance(mass_tolerance)

            #
            # Get peak intensity for each isotopomer in each spectrum ID in each peptide
            #
            peaks.get_isotopes_from_amrt_multiwrapper(num_thread=num_thread)

            # Create subdirectory if not exists
            os.makedirs(os.path.join(directory_to_write, current_sample), exist_ok=True)
            save_path = os.path.join(directory_to_write, current_sample, mzml_files[idx] + '_riana.txt')
            peaks.id_result_df.to_csv(save_path, sep='\t')

            # Make the soft-threshold data frame. These are the peptides that are ID'ed at 10 times the q-value
            # as the cut-off in this fraction up to q < 0.1, but has q >= q-value cutoff, and furthermore has been
            # consistently identified in the other samples at the same fraction (median fraction) at the q-value cutoff




    return sys.exit(os.EX_OK)


#
# Code for running main with parsed arguments from command line
#
def main():

    import argparse

    parser = argparse.ArgumentParser(description='Riana integrates the relative abundance of'
                                                 'isotopomers')

    parser.add_argument('dir', help='path to folders containing the mzml and search files (see documentation)')

    # parser.add_argument('mzml', help='path to folder containing mzml files')

    parser.add_argument('-i', '--iso', help='isotopes to do, separated by commas, e.g., 0,1,2,3,4,5 [default: 0,6]',
                              default='0,6')

    parser.add_argument('-u', '--unique', action='store_true', help='integrate unique peptides only')

    parser.add_argument('--amrt', action='store_true', help='integrate an inclusion list of AM-RTs',
                        default=False)

    parser.add_argument('-k', '--lysine',
                        help='lysine mode, 0=No filter, 1=1 K, 2=1 or more K, 3=KK only [default = 0]',
                        type=int,
                        choices=[0, 1, 2, 3],
                        default=0)

    '''
    parser.add_argument('-t', '--test', action='store_true',
                        help='test mode: integrates only first 50 qualifying peptides')
    '''

    parser.add_argument('--matchbetweenruns', action='store_true', help='attempt to match between runs',
                        default=False)

    parser.add_argument('-q', '--qvalue',
                        help='integrate only peptides with q value below this threshold[default: 1e-2]',
                        type=float,
                        default=1e-2)

    parser.add_argument('-r', '--rtime', help='retention time (in minutes, both directions) tolerance for integration',
                        type=float,
                        default=1.0)

    parser.add_argument('-m', '--masstolerance', help='mass tolerance in ppm for integration [default 100 ppm]',
                        type=float,
                        default=100)

    parser.add_argument('-t', '--thread', help='thread (default = 4)',
                        type=float,
                        default=4.0)


    parser.add_argument('-o', '--out', help='prefix of the output directory [default: riana_out]',
                        default='riana_out')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {version}'.format(version=__version__))

    parser.set_defaults(func=runRiana)

    # Print help message if no arguments are given
    import sys
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    #gc.enable()
    #gc.set_debug(gc.DEBUG_LEAK)

    # Parse all the arguments
    args = parser.parse_args()

    # Run the function in the argument
    args.func(args)
