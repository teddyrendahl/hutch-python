============
Hutch Python
============
.. image:: https://travis-ci.org/pcdshub/hutch-python.svg?branch=master
   :target: https://travis-ci.org/pcdshub/hutch-python
   :alt: Build Status
.. image:: https://codecov.io/gh/pcdshub/hutch-python/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pcdshub/hutch-python
   :alt: Code Coverage
.. image:: https://landscape.io/github/pcdshub/hutch-python/master/landscape.svg?style=flat
   :target: https://landscape.io/github/pcdshub/hutch-python/master
   :alt: Code Health

Hutch Python is the launcher and config reader for LCLS interactive IPython
sessions. This will replace the existing Python 2 ``pyhutch`` modules
(blbase/blutil/blinst) for scripting during experiments.

Requirements
------------

This module is intended to be run using the latest pcds release in the
`pcds-envs <https://github.com/pcdshub/pcds-envs>`_ package, but this is not
strictly required. Other than Python 3.6+, there are few requirements for
running this module. These are small utilities:

- ``ipython``, for improved interactive sessions
- ``pyyaml``, for reading config files
- ``coloredlogs``, for colored logging

At LCLS, there is little point to running this module without:

- `pcdsdevices <https://github.com/pcdshub/pcdsdevices>`_ for our Device abstraction layers
- ``pydaq`` for running the DAQ
- `bluesky <https://github.com/nsls-ii/bluesky>`_ for scanning

If present, some modules will enable extra features, which will be listed
below:

- None, at the moment

In the future, I plan to support the following extra features:

- `happi <https://github.com/slaclab/happi>`_ will enable device loading from a happi database, and from the experiment questionaire.
- `lightpath <https://github.com/slaclab/lightpath>`_ will enable specification of a path object to include (requires happi).
- ``pyfiglet`` will enable hutch banners (think big ``xpppython`` on startup)


Installation
------------

This module is not yet ready for users. When completed, the included conda
recipe will install all optional requirements by default. It is assumed that
every user will want all of the features. It is up to you to install this
module differently if you do not want the added dependencies. In the future,
this will be installable via conda channel.
