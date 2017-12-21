import logging
import os.path

from hutch_python.load_conf import load, read_conf

logger = logging.getLogger(__name__)


def test_load_normal():
    logger.debug('test_load_normal')
    objs = load(os.path.join(os.path.dirname(__file__), 'conf.yaml'))
    should_have = ('x', 's', 'scripts', 'm', 'motors', 'p', 'pims', 's',
                   'slits', 'f', 'fake', 'fake_motor', 'fake_det',
                   'unique_device', 'calc_thing')
    for elem in should_have:
        assert elem in objs
    assert objs['s'] == objs['scripts']
    assert len(objs['fake'].__dict__) == 2


def test_read_empty():
    logger.debug('test_read_empty')
    objs = read_conf({})
    assert objs == {}


def test_read_duplicate():
    logger.debug('test_read_duplicate')
    objs = read_conf({'load': ['sample_module_1.py', 'sample_module_1.py']})
    assert len(objs) == 3


def test_read_only_namespaces():
    logger.debug('test_read_only_namespaces')
    objs = read_conf({'namespace': {'class': {'float': ['text', 'words']}}})
    assert len(objs) == 2
