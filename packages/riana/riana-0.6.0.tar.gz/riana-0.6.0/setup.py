from setuptools import setup
from riana import __version__

setup(
   name='riana',
   version=__version__,
   description='Riana integrates the relative abundance of isotopomers',
   author='Edward Lau',
   url='https://www.laulab.net',
   author_email='edward.lau@cuanschutz.edu',
   packages=['riana'],  #same as name
   install_requires=['pymzml', 'scipy', 'pandas', 'matplotlib', 'tqdm', 'sklearn'], #external packages as dependencies
)
