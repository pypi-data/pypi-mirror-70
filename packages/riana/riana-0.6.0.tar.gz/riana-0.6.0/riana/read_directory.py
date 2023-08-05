import os


class ReadDirectory(object):
    """
    This class reads the Project Directory and find the Percolator and mzML files inside. We needed some kindof
    structure in order to do match between run functionality.

    """

    def __init__(self, path):
        """
        :param path: path of the project folder, e.g., "~/Desktop/example/"


        """
        self.path = os.path.join(path)
        self.samples = self.get_sample_list()

    def get_sample_list(self):
        """
        Get the list of samples and check that each is a directory
        :return:
        """

        sample_list = [s for s in sorted(os.listdir(self.path)) if s != '.DS_Store']

        for sample in sample_list:
            sample_loc = os.path.join(self.path, sample)
            assert os.path.isdir(sample_loc), '[error] project sample subdirectory not valid'

        return sample_list
