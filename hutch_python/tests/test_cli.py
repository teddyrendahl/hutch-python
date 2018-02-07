import os
import logging

import pytest

from hutch_python.cli import setup_cli_env, hutch_ipython_embed

from conftest import cli_args, restore_logging

logger = logging.getLogger(__name__)


def test_setup_cli():
    logger.debug('test_setup_cli')

    cfg = os.path.dirname(__file__) + '/conf.yaml'
    db = os.path.dirname(__file__) + '/happi_db.json'

    with cli_args(['hutch_python', '--cfg', cfg, '--db', db]):
        with restore_logging():
            setup_cli_env()


def test_debug_arg():
    logger.debug('test_debug_arg')

    cfg = os.path.dirname(__file__) + '/conf.yaml'
    db = os.path.dirname(__file__) + '/happi_db.json'

    with cli_args(['hutch_python', '--cfg', cfg, '--db', db, '--debug']):
        with restore_logging():
            setup_cli_env()


def test_hutch_ipython_embed():
    logger.debug('test_hutch_ipython_embed')

    # OSError because we can't actually enter IPython here.
    # Any other error means something bad happened.
    with pytest.raises(OSError):
        hutch_ipython_embed()
