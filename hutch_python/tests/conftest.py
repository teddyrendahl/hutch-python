import os
import sys
import logging
from copy import copy
from contextlib import contextmanager
from collections import namedtuple
from logging.handlers import QueueHandler
from queue import Queue

import pytest

import hutch_python.utils

# We need to have the tests directory importable to match what we'd have in a
# real hutch-python install
sys.path.insert(0, os.path.dirname(__file__))


@contextmanager
def cli_args(args):
    """
    Context manager for running a block of code with a specific set of
    command-line arguments.
    """
    prev_args = sys.argv
    sys.argv = args
    yield
    sys.argv = prev_args


@contextmanager
def restore_logging():
    """
    Context manager for reverting our logging config after testing a function
    that configures the logging.
    """
    prev_handlers = copy(logging.root.handlers)
    yield
    logging.root.handlers = prev_handlers


@pytest.fixture(scope='function')
def log_queue():
    with restore_logging():
        my_queue = Queue()
        handler = QueueHandler(my_queue)
        root_logger = logging.getLogger('')
        root_logger.addHandler(handler)
        yield my_queue


Experiment = namedtuple('Experiment', ('run', 'proposal',
                                       'user', 'pw', 'kerberos'))


class QSBackend:
    empty = False

    def __init__(self, run, proposal, use_kerberos=True, user=None, pw=None):
        self.run = run
        self.proposal = proposal
        self.user = user
        self.pw = pw
        self.kerberos = use_kerberos

    def find(self, multiples=False, **kwargs):
        devices = [{
            '_id': 'TST:USR:MMN:01',
            'beamline': 'TST',
            'device_class': 'hutch_python.tests.conftest.Experiment',
            'location': 'Hutch-main experimental',
            'args': ['{{run}}', '{{proposal}}',
                     '{{user}}', '{{pw}}', '{{kerberos}}'],
            'kwargs': {},
            'name': 'inj_x',
            'prefix': 'TST:USR:MMN:01',
            'purpose': 'Injector X',
            'type': 'Device',
            'run': self.run,
            'user': self.user,
            'pw': self.pw,
            'kerberos': self.kerberos,
            'proposal': self.proposal}]
        if self.empty:
            return None
        elif multiples:
            return devices
        else:
            return devices[0]


cfg = """\
[DEFAULT]
user=user
pw=pw
"""


@pytest.fixture(scope='function')
def temporary_config():
    # Write to our configuration
    with open('web.cfg', '+w') as f:
        f.write(cfg)
    # Allow the test to run
    yield
    # Remove the file
    os.remove('web.cfg')


@pytest.fixture(scope='function')
def fake_curexp_script():
    old_script = hutch_python.utils.CUR_EXP_SCRIPT
    hutch_python.utils.CUR_EXP_SCRIPT = 'echo {}lr1215'
    yield
    hutch_python.utils.CUR_EXP_SCRIPT = old_script
