============
Hutch Python
============
.. image:: https://travis-ci.org/pcdshub/hutch-python.svg?branch=master
   :target: https://travis-ci.org/pcdshub/hutch-python
   :alt: Build Status
.. image:: https://codecov.io/gh/pcdshub/hutch-python/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pcdshub/hutch-python
   :alt: Code Coverage

``hutch-python`` is the launcher and config reader for LCLS interactive IPython
sessions.

Requirements
------------

This module is intended to be run using the latest pcds release in the
`pcds-envs <https://github.com/pcdshub/pcds-envs>`_ package.

This module requires Python 3.6+ and the following utilities:

- ``ipython``, for improved interactive sessions
- `pcdsdaq <https://github.com/pcdshub/pcdsdaq>`_
  for using the daq in scans
- `pcdsdevices <https://github.com/pcdshub/pcdsdevices>`_
  for our Device abstraction layers
- `happi <https://github.com/pcdshub/happi>`_
  to enable device loading from a happi database
- `psdm_qs_cli <https://github.com/slaclab/psdm_qs_cli>`_
  as an optional happi dependency for loading from the experiment
  questionnaire
- `lightpath <https://github.com/pcdshub/lightpath>`_
  organizes devices to provide a summarized state of the beamline as a whole
- ``pyyaml``, for reading config files
- ``coloredlogs``, for colored logging
- ``pyfiglet`` for hutch banners (think big ``xpppython`` on startup)
- `cookiecutter <https://github.com/audreyr/cookiecutter>`_
  for starting new hutch repos

To connect to the LCLS DAQ, your environment must have access to

- ``pydaq`` for connecting to and running the daq
- ``pycdb`` for changing daq object configurations
- ``pyami`` for viewing data from the daq

These are not available outside of the slac intranet, and in some cases
must be sync'd with the active DAQ versions, independent of all other
packages.

To automatically select the current experiment, you must run with access to
the LCLS NFS directories.

Installation
------------

The easiest way to install ``hutch-python`` is through
`conda <https://conda.io/docs>`_, which is easy to
`install <https://conda.io/miniconda.html>`_. The requirements have not yet
been consolidated into one conda channel, but we plan to place everything in
the ``pcds-tag`` channel in the future. Currently, to pick up all
dependencies, run this command:

``conda install hutch-python -c pcds-tag -c pydm-tag -c lightsource2-tag
-c defaults -c conda-forge``
