import logging

from hutch_python.log_setup import (DEFAULT_YAML, DIR_LOGS,
                                    setup_logging, set_console_level)

from conftest import restore_logging

logger = logging.getLogger(__name__)


def test_setup_logging():
    logger.debug('test_setup_logging')

    with restore_logging():
        setup_logging(path_yaml=DEFAULT_YAML)

    assert DIR_LOGS.exists()


def test_set_console_level(log_queue):
    logger.debug('test_set_console_level')

    root_logger = logging.getLogger('')
    queue_handler = root_logger.handlers[-1]
    queue_handler.name = 'console'
    queue_handler.level = 20

    # Clear the queue
    while not log_queue.empty():
        log_queue.get(block=False)

    # Sanity
    logger.info('hello')
    logger.debug('goodbye')
    assert 'hello' in log_queue.get(block=False).getMessage()
    assert log_queue.empty()

    # Change console level so we get debug statements
    set_console_level(10)
    logger.debug('goodbye')
    assert 'goodbye' in log_queue.get(block=False).getMessage()
