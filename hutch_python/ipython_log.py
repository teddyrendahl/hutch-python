"""
IPython plugin to log inputs, outputs, and tracebacks to the debug stream.
"""
import sys
import traceback
import logging

import IPython

import __main__

logger = logging.getLogger(__name__)


class IPythonLogger:
    def __init__(self):
        self.prev_err = None

    def log(self):
        line_num = len(__main__.In) - 1
        if line_num == 0:
            return
        last_in = __main__.In[-1]
        logger.debug('In  [{}]: {}'.format(line_num, last_in))
        try:
            last_out = __main__.Out[line_num]
            # Convert to string, limit to max tweet length
            last_out = str(last_out)[:280]
            logger.debug('Out [{}]: {}'.format(line_num, last_out))
        except KeyError:
            pass
        global PREV_ERR
        if hasattr(sys, 'last_value') and sys.last_value != self.prev_err:
            tb = ''.join(traceback.format_exception(sys.last_type,
                                                    sys.last_value,
                                                    sys.last_traceback))
            logger.debug('Exception in IPython session, traceback:\n' + tb)
            self.prev_err = sys.last_value


def init_ipython_logger():
    ip = IPython.get_ipython()
    ip.events.register('post_execute', IPythonLogger().log)
