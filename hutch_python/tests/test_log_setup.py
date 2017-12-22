import logging

from hutch_python.log_setup import DEFAULT_YAML, DIR_LOGS, setup_logging

from conftest import restore_logging

logger = logging.getLogger(__name__)


def test_setup_logging():
    logger.debug('test_setup_logging')

    with restore_logging():
        setup_logging(path_yaml=DEFAULT_YAML)

    assert DIR_LOGS.exists()
