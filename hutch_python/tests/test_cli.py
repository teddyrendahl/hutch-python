import os
import shutil
import logging
from pathlib import Path

import pytest

from hutch_python.cli import (setup_cli_env, hutch_ipython_embed, run_script,
                              start_user)
from hutch_python.load_conf import load

from conftest import cli_args, restore_logging

logger = logging.getLogger(__name__)

CFG_PATH = Path(os.path.dirname(__file__)) / 'conf.yaml'
CFG = str(CFG_PATH)


def test_setup_cli_normal():
    logger.debug('test_setup_cli')

    with cli_args(['hutch_python', '--cfg', CFG]):
        with restore_logging():
            setup_cli_env()


def test_setup_cli_no_args():
    logger.debug('test_setup_cli_no_args')

    with cli_args(['hutch_python']):
        with restore_logging():
            setup_cli_env()


def test_debug_arg():
    logger.debug('test_debug_arg')

    with cli_args(['hutch_python', '--cfg', CFG, '--debug']):
        with restore_logging():
            setup_cli_env()


def test_sim_arg():
    logger.debug('test_sim_arg')

    with cli_args(['hutch_python', '--cfg', CFG, '--sim']):
        with restore_logging():
            setup_cli_env()


def test_create_arg():
    logger.debug('test_create_arg')

    hutch = 'temp_create'
    test_dir = CFG_PATH.parent.parent.parent / hutch
    if test_dir.exists():
        shutil.rmtree(test_dir)

    with cli_args(['hutch_python', '--create', hutch]):
        with restore_logging():
            setup_cli_env()

    assert test_dir.exists()

    load(str(test_dir / 'conf.yml'))
    shutil.rmtree(test_dir)


def test_hutch_ipython_embed():
    logger.debug('test_hutch_ipython_embed')

    # OSError because we can't actually enter IPython here.
    # Any other error means something bad happened.
    with pytest.raises(OSError):
        hutch_ipython_embed()


def test_run_script():
    logger.debug('test_run_script')

    # Setting the name that script.py needs should avoid a NameError because
    # this is supposed to run the script in the enclosing frame
    unique_device = 4  # NOQA
    run_script(Path(__file__).parent / 'script.py')


def test_start_user():
    logger.debug('test_start_user')

    with cli_args(['hutch_python', '--cfg', CFG]):
        with restore_logging():
            setup_cli_env()

    # OSError from opening ipython shell
    with pytest.raises(OSError):
        start_user()

    script = str(Path(__file__).parent / 'script.py')

    with cli_args(['hutch_python', '--cfg', CFG, script]):
        with restore_logging():
            setup_cli_env()

    # No OSError because we're just running a print script
    # Setting the name that script.py needs should avoid a NameError because
    # this is supposed to run the script in the enclosing frame
    unique_device = 4  # NOQA
    start_user()
