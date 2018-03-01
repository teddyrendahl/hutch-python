============
Hutch Python
============
.. image:: https://travis-ci.org/pcdshub/hutch-python.svg?branch=master
   :target: https://travis-ci.org/pcdshub/hutch-python
   :alt: Build Status
.. image:: https://codecov.io/gh/pcdshub/hutch-python/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pcdshub/hutch-python
   :alt: Code Coverage

Hutch Python is the launcher and config reader for LCLS interactive IPython
sessions. This will replace the existing Python 2 ``pyhutch`` modules
(blbase/blutil/blinst) for scripting during experiments.

Requirements
------------

This module is intended to be run using the latest pcds release in the
`pcds-envs <https://github.com/pcdshub/pcds-envs>`_ package.

This module requires Python 3.6+ and the following utilities:

- ``ipython``, for improved interactive sessions
- ``pyyaml``, for reading config files
- ``coloredlogs``, for colored logging
- `pcdsdevices <https://github.com/pcdshub/pcdsdevices>`_ for our Device abstraction layers
- ``pydaq`` for running the DAQ
- `happi <https://github.com/slaclab/happi>`_ to enable device loading from a
   happi database, and from the experiment questionaire.
- `bluesky <https://github.com/nsls-ii/bluesky>`_ for scanning
- ``pyfiglet`` for hutch banners (think big ``xpppython`` on startup)
- `lightpath <https://github.com/slaclab/lightpath>`_ organizes devices
  devices to provide a summarized state of the beamline as a whole

Installation
------------

This module is not yet ready for users. When completed, the included conda
recipe will install all optional requirements by default. It is assumed that
every user will want all of the features. It is up to you to install this
module differently if you do not want the added dependencies. In the future,
this will be installable via conda channel.
