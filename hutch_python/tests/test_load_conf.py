import logging
import os.path
from types import SimpleNamespace

import hutch_python.qs_load
from hutch_python.load_conf import load, load_conf

from .conftest import QSBackend

logger = logging.getLogger(__name__)


def test_file_load():
    logger.debug('test_file_load')
    objs = load(os.path.join(os.path.dirname(__file__), 'conf.yaml'))
    should_have = ('x', 'unique_device', 'calc_thing', 'daq', 'tst_beampath')
    err = '{} was overriden by a namespace'
    for elem in should_have:
        assert not isinstance(objs[elem], SimpleNamespace), err.format(elem)


def test_no_file():
    logger.debug('test_no_file')
    objs = load()
    assert len(objs) > 1


def test_conf_empty():
    logger.debug('test_conf_empty')
    objs = load_conf({})
    assert len(objs) > 1


def test_skip_failures():
    logger.debug('test_skip_failures')
    # Should not raise
    load_conf(dict(hutch=345243, db=12351324, experiment=2341234, load=123454,
                   bananas='dole'))


def test_auto_experiment(fake_curexp_script):
    logger.debug('test_auto_experiment')
    hutch_python.qs_load.QSBackend = QSBackend
    objs = load_conf(dict(hutch='tst'))
    assert objs['inj_x'].run == '15'
    assert objs['inj_x'].proposal == 'LR12'


def test_cannot_auto():
    logger.debug('test_cannot_auto')
    # Fail silently
    load_conf(dict(hutch='tst'))
