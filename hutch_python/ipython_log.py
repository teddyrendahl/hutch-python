"""
IPython plugin to log inputs, outputs, and tracebacks to the debug stream.
"""
import sys
import traceback
import logging

logger = logging.getLogger(__name__)


class IPythonLogger:
    def __init__(self, ipython):
        self.prev_err = None
        self.In = ipython.user_ns['In']
        self.Out = ipython.user_ns['Out']

    def log(self):
        try:
            line_num = len(self.In) - 1
            if line_num == 0:
                return
            last_in = self.In[-1]
            logger.debug('In  [{}]: {}'.format(line_num, last_in))
            try:
                last_out = self.Out[line_num]
                # Convert to string, limit to max tweet length
                last_out = str(last_out)[:280]
                logger.debug('Out [{}]: {}'.format(line_num, last_out))
            except KeyError:
                pass
            if hasattr(sys, 'last_value') and sys.last_value != self.prev_err:
                tb = ''.join(traceback.format_exception(sys.last_type,
                                                        sys.last_value,
                                                        sys.last_traceback))
                logger.debug('Exception in IPython session, traceback:\n' + tb)
                self.prev_err = sys.last_value
        except Exception:
            logger.debug('Logging error', show_exc=True)


def init_ipython_logger(ip):
    ip.events.register('post_execute', IPythonLogger(ip).log)
