import logging

from hutch_python.yaml_file import load_objs

logger = logging.getLogger(__name__)


def test_file_load():
    logger.debug('test_file_load')
    info = ['sample_module_1.py', 'sample_module_2.py']
    objs = load_objs(info)
    assert objs['hey'] == '4horses'
    assert objs['milk'] == 'cows'
    assert objs['some_int'] == 5
    assert objs['just_this'] == 5.0
