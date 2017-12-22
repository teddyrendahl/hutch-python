Logging Configuration
=====================

The logging configuration is specified in the
top-level ``logging.yaml`` file using the
`dictConfig <https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig>`_
spec. There is also a testing logger that is set up directly in the
``run_tests.py`` file.

As a summary, the logger is set up to:

- Use coloredlogs default colors to print INFO log level and message
- Create rotating file handlers for each log level (and above)
- Store logs in the user's launch directory's ``logs`` folder

The tests logger is set up to:

- Log with level DEBUG to the diractory's ``logs`` folder
- Rotate the file such that each testing run has its own log file

There is a helper module ``log_setup`` that is used internally to set up the
logger for interactive sessions.

log_setup.py
------------
.. autofunction::
   hutch_python.log_setup.setup_logging
