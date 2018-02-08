import os
import logging
from pathlib import Path

import pytest

from hutch_python.cli import (setup_cli_env, hutch_ipython_embed, run_script,
                              start_user)

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


def test_run_script():
    logger.debug('test_run_script')
    # Checking the output happens in test_tstpython, just make sure we can get
    # through the code without an exception for coverage
    run_script(Path(__file__).parent / 'script.py')


def test_start_user():
    logger.debug('test_start_user')

    cfg = os.path.dirname(__file__) + '/conf.yaml'
    db = os.path.dirname(__file__) + '/happi_db.json'

    with cli_args(['hutch_python', '--cfg', cfg, '--db', db]):
        with restore_logging():
            setup_cli_env()

    # OSError from opening ipython shell
    with pytest.raises(OSError):
        start_user()

    script = str(Path(__file__).parent / 'script.py')

    with cli_args(['hutch_python', '--cfg', cfg, '--db', db, script]):
        with restore_logging():
            setup_cli_env()

    # No OSError because we're just running a print script
    start_user()
