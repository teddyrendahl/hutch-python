import os
import time
import logging
import logging.config
from contextlib import contextmanager
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

DIR_MODULE = Path(__file__).resolve().parent
FILE_YAML = DIR_MODULE / 'logging.yml'


def setup_logging(dir_logs=None):
    """
    Sets up the logging module to make a properly configured logger using the
    ``logging.yml`` configuration.

    Parameters
    ----------
    dir_logs : str or Path, optional
        Path to the log directory. If omitted, we won't use a log file.
    """
    with open(FILE_YAML, 'rt') as f:
        config = yaml.safe_load(f.read())

    if dir_logs is None:
        # Remove debug file from the config
        del config['handlers']['debug']
        config['root']['handlers'].remove('debug')
    else:
        # Ensure Path object
        dir_logs = Path(dir_logs)

        # Subdirectory for year/month
        dir_month = dir_logs / time.strftime('%Y_%m')

        # Make the log directories if they don't exist
        # Make sure each level is all permissions
        for directory in (dir_logs, dir_month):
            if not directory.exists():
                directory.mkdir()
                directory.chmod(0o777)

        user = os.environ['USER']
        timestamp = time.strftime('%d_%Hh%Mm%Ss')
        log_file = '{}_{}.{}'.format(user, timestamp, 'log')
        path_log_file = dir_month / log_file
        path_log_file.touch()
        config['handlers']['debug']['filename'] = str(path_log_file)

    logging.config.dictConfig(config)


def get_console_handler():
    root = logging.getLogger('')
    for handler in root.handlers:
        if handler.name == 'console':
            return handler
    raise RuntimeError('No console handler')


def get_console_level():
    handler = get_console_handler()
    return handler.level


def set_console_level(level=logging.INFO):
    handler = get_console_handler()
    handler.level = level


def debug_mode(debug=None):
    if debug is None:
        level = get_console_level()
        return level <= logging.DEBUG
    elif debug:
        set_console_level(level=logging.DEBUG)
    else:
        set_console_level(level=logging.INFO)


@contextmanager
def debug_context():
    old_level = get_console_level()
    debug_mode(True)
    yield
    set_console_level(level=old_level)


def debug_wrapper(f, *args, **kwargs):
    with debug_context():
        f(*args, **kwargs)
