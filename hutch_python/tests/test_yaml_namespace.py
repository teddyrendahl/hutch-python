import logging

import pytest

from hutch_python.yaml_namespace import NameSpaceAssembler


logger = logging.getLogger(__name__)
objs = {'catagory': {'one': 1, 'two': 2.0, 'three': '3'},
        'my_list': ['apples', 4]}
info = {'catagory': ['cat', 'dog'],
        'class': {'float': ['flt'],
                  'str': ['sting']}}


@pytest.fixture(scope='func')
def assembler():
    return NameSpaceAssembler(info)


def test_source_space(assembler):
    logger.debug('test_source_space')
    namespaces = assembler.source_space(objs['catagory'], info['catagory'])
    assert 'cat' in namespaces
    space = namespaces['dog']
    assert space.one == 1
    assert space.two == 2.0
    assert space.three == '3'


def test_class_space(assembler):
    logger.debug('test_class_space')
    namespaces = assembler.class_space(objs, info['class'])
    float_space = namespaces['flt']
    assert float_space.two == 2.0
    string_space = namespaces['sting']
    assert string_space.three == '3'
    assert string_space.str == 'apples'


def test_assemble(assembler):
    logger.debug('test_assemble')
    namespaces = assembler.assemble(objs)
    cat_space = namespaces['cat']
    dog_space = namespaces['dog']
    flt_space = namespaces['flt']
    sting_space = namespaces['sting']
    assert cat_space.one == 1
    assert cat_space.two == 2.0
    assert cat_space.three == '3'
    assert dog_space.one == 1
    assert dog_space.two == 2.0
    assert dog_space.three == '3'
    assert flt_space.two == 2.0
    assert sting_space.three == '3'
    assert sting_space.str == 'apples'
