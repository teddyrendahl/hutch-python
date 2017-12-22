import logging
from types import SimpleNamespace

import pytest

from hutch_python.plugins.namespace import Plugin, NamespaceManager


logger = logging.getLogger(__name__)


def test_namespace_plugin_manager():
    logger.debug('test_namespace_plugin_base')

    space = SimpleNamespace()
    manager = NamespaceManager(space, 'test')
    with pytest.raises(NotImplementedError):
        manager.should_include('name', 'obj')


def test_namespace_plugin_class():
    logger.debug('test_namespace_plugin_class')
    objs = {'one': 1, 'two': 2.0, 'three': '3'}
    info = {'class': {'float': ['flt'],
                      'skip_bad': ['skip_me'],
                      'str': ['text', 'words']}}
    plugin = Plugin(info)
    namespaces = plugin.get_objects()
    plugin.future_plugin_hook(None, objs)
    float_space = namespaces['flt']
    assert float_space.two == 2.0
    string_space = namespaces['text']
    assert string_space.three == '3'
    assert string_space == namespaces['words']
