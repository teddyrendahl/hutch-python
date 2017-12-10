import versioneer
from setuptools import setup, find_packages

setup(name='hutch-python',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      license='BSD',
      author='SLAC National Accelerator Laboratories',
      packages=find_packages(),
      description=('Launcher and Config Reader for '
                   'LCLS Interactive IPython Sessions'),
      scripts=['bin/hutch-python']
      )
