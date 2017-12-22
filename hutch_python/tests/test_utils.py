import logging

from hutch_python import utils

logger = logging.getLogger(__name__)


def test_extract_objs():
    logger.debug('test_extract_objs')
    # Has no __all__ keyword
    objs = utils.extract_objs('sample_module_1')
    assert objs == dict(hey='4horses',
                        milk='cows',
                        some_int=5)
    # Has an __all__ keyword
    objs = utils.extract_objs('sample_module_2.py')
    assert objs == dict(just_this=5.0)
    # Doesn't exist
    objs = utils.extract_objs('fake_module_243esd')
    assert objs == {}


def test_find_class():
    logger.debug('test_find_class')
    # Find some standard type that needs an import
    found_Request = utils.find_class('urllib.request.Request')
    from urllib.request import Request
    assert found_Request is Request
    # Find some built-in type
    found_float = utils.find_class('float')
    assert found_float is float
