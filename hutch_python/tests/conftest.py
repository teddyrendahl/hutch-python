import os
import sys
import logging
from copy import copy
from contextlib import contextmanager
from collections import namedtuple

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


Experiment = namedtuple('Experiment', ('run', 'proposal'))


class QSBackend:
    def __init__(self, run, proposal):
        self.run = run
        self.proposal = proposal

    def find(self, multiples=False, **kwargs):
        devices = [{
            '_id': 'TST:USR:MMN:01',
            'beamline': 'TST',
            'device_class': 'hutch_python.tests.conftest.Experiment',
            'location': 'Hutch-main experimental',
            'args': ['{{run}}', '{{proposal}}'],
            'kwargs': {},
            'name': 'inj_x',
            'prefix': 'TST:USR:MMN:01',
            'purpose': 'Injector X',
            'type': 'Device',
            'run': self.run,
            'proposal': self.proposal}]
        if multiples:
            return devices
        else:
            return devices[0]
