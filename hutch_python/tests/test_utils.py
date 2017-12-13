import logging

import pytest

from hutch_python import utils

logger = logging.getLogger(__name__)


def test_interpret_list():
    logger.debug('test_interpret_list')
    test_input = 'apples to apples'
    answer = ['apples', 'to', 'apples']
    junk = 234453
    assert utils.interpret_list(test_input) == answer
    assert utils.interpret_list(answer) == answer
    with pytest.raises(RuntimeError):
        utils.interpret_list(junk)


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


class Named:
    def __init__(self, *, name):
        self.name = name


def test_assign_names():
    logger.debug('test_assign_names')
    obj = Named(name='Karl')
    num = 2.3
    name_dict = utils.assign_names([obj, num])
    assert name_dict == dict(Karl=obj, float=num)


def test_find_class():
    logger.debug('test_find_class')
    # Find some standard type that needs an import
    found_Request = utils.find_class('urllib.request.Request')
    from urllib.request import Request
    assert found_Request is Request
    # Find some built-in type
    found_float = utils.find_class('float')
    assert found_float is float
