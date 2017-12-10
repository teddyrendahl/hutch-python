===============================
Hutch Python
===============================

Launcher and Config Reader for LCLS Interactive IPython Sessions. This will replace the existing Python 2 pyhutch modules (blbase/blutil/blinst) for scripting during experiments.

Overview
--------
Stay tuned.

Requirements
------------

This module is intended to be run using the latest pcds release in the `pcds-envs <https://github.com/pcdshub/pcds-envs>`_ package, but this is not strictly required.
Other than Python 3.5+, there are few requirements for running this module. These are small utilities:

- coloredlogs, for colored logging

If present, some modules will enable extra features, which will be listed below:

- `happi <https://github.com/slaclab/happi>`_ will enable device loading from a happi database. Requires all modules of included devices.
- `lightpath <https://github.com/slaclab/lightpath>`_ will enable specification of a path object to include (requires happi).


Installation
------------

In the future, this will be installable via conda channel. Stay tuned.

Running the Tests
-----------------
::

  $ python run_tests.py
