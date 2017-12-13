import logging
import os.path

from hutch_python.load_conf import load, read_conf

logger = logging.getLogger(__name__)


def test_load_normal():
    logger.debug('test_load_normal')
    objs = load(os.path.join(os.path.dirname(__file__), 'conf.yml'))
    assert objs['hey'] == '4horses'
    assert objs['milk'] == 'cows'
    assert objs['some_int'] == 5
    assert objs['just_this'] == 5.0
    assert 'sample_plan' in objs
    assert 'cat' in objs
    assert 'dog' in objs
    assert 'flt' in objs
    assert 'sting' in objs


def test_read_empty():
    logger.debug('test_read_empty')
    objs = read_conf({})
    assert objs == {}


def test_read_duplicate():
    logger.debug('test_read_duplicate')
    objs = read_conf({'file': ['sample_module_1.py', 'sample_module_1.py']})
    assert len(objs) == 3


def test_read_only_namespaces():
    logger.debug('test_read_only_namespaces')
    objs = read_conf({'namespace': {'file': ['beamline'],
                                    'class': {'float': ['flt']}}})
    assert len(objs) == 2
