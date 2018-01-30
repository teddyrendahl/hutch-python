import logging

import pytest

from hutch_python import register_load, clear_load
import hutch_python

logger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def clear():
    clear_load()
    yield
    clear_load()


def test_register_once(clear):
    register_load('apples', {'a': 'a', 'b': 'b'})
    assert hutch_python.apples.a == 'a'
    assert hutch_python.apples.b == 'b'


def test_register_twice(clear):
    register_load('apples', {'a': 'a', 'b': 'b'})
    register_load('apples', {'c': 'c', 'd': 'd'})
    assert hutch_python.apples.a == 'a'
    assert hutch_python.apples.b == 'b'
    assert hutch_python.apples.c == 'c'
    assert hutch_python.apples.d == 'd'
