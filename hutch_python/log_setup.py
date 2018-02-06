import os
import time
import logging
import logging.config
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

DIR_MODULE = Path(__file__).resolve().parent
DEFAULT_YAML = DIR_MODULE / 'logging.yml'
DIR_LOGS = DIR_MODULE / 'logs'


def setup_logging(path_yaml=None, dir_logs=None, default_level=logging.INFO):
    """
    Sets up the logging module to make a properly configured logger.

    This will go into the ``logging.yml`` file in the this directory, and
    try to load the logging configuration. If it fails for any reason, it will
    just use the default configuration. For more details on how the logger will
    be configured, see the ``logging.yml`` file.

    Parameters
    ----------
    path_yaml : str or Path, optional
        Path to the yaml file.

    dir_logs : str or Path, optional
        Path to the log directory.

    default_level : logging.LEVEL, optional
        Logging level for the default logging setup if the yaml fails.
    """
    # Get the yaml path
    if path_yaml is None:
        path_yaml = DEFAULT_YAML
    # Make sure we are using Path objects
    else:
        path_yaml = Path(path_yaml)
    # Get the log directory
    if dir_logs is None:
        dir_logs = DIR_LOGS
    # Make sure we are using Path objects
    else:
        dir_logs = Path(dir_logs)

    # Make the log directory if it doesn't exist
    if not dir_logs.exists():
        dir_logs.mkdir()

    with open(path_yaml, 'rt') as f:
        config = yaml.safe_load(f.read())

    user = os.environ['USER']
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    log_file = '{}_{}.{}'.format(user, timestamp, 'debug')
    path_log_file = dir_logs / (log_file + '.log')
    path_log_file.touch()
    config['handlers']['debug']['filename'] = str(path_log_file)

    logging.config.dictConfig(config)
