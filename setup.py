import versioneer
from setuptools import setup, find_packages

setup(name='hutch-python',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      license='BSD',
      author='SLAC National Accelerator Laboratories',
      packages=find_packages(),
      description='Laucher and Config Reader for LCLS Python 3 Interactive IPython Sessions',
      )
