import os
import logging

from hutch_python.cli import setup_cli_env

from conftest import cli_args, restore_logging

logger = logging.getLogger(__name__)


def test_setup_cli():
    logger.debug('test_setup_cli')

    cfg = os.path.dirname(__file__) + '/conf.yaml'
    db = os.path.dirname(__file__) + '/happi_db.json'

    with cli_args(['hutch_python', '--cfg', cfg, '--db', db]):
        with restore_logging():
            setup_cli_env()
