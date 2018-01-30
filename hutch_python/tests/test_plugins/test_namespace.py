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
    conf = dict(namespace=info)
    plugin = Plugin(conf)
    namespaces = plugin.get_objects()
    plugin.future_plugin_hook(None, objs)
    float_space = namespaces['flt']
    assert float_space.two == 2.0
    string_space = namespaces['text']
    assert string_space.three == '3'
    assert string_space == namespaces['words']


def test_namespace_plugin_metadata():
    logger.debug('test_namespace_plugin_metadata')
    obj1 = SimpleNamespace()
    obj2 = SimpleNamespace()
    obj3 = SimpleNamespace()
    obj4 = SimpleNamespace()
    obj5 = SimpleNamespace()
    obj1.md = SimpleNamespace(beamline='MFX', stand='DIA')
    obj2.md = SimpleNamespace(beamline='MFX', stand='DIA')
    obj3.md = SimpleNamespace(beamline='MFX', stand='DG2')
    obj4.md = SimpleNamespace(beamline='MFX')
    obj5.md = SimpleNamespace(beamline='XPP', stand='SB2')
    objs = dict(mfx_dia_obj1=obj1, mfx_dia_obj2=obj2, mfx_dg2_obj3=obj3,
                mfx_obj4=obj4, xpp_sb2_obj5=obj5)
    info = {'metadata': ['beamline', 'stand']}
    plugin = Plugin(info=info)
    namespaces = plugin.get_objects()
    plugin.future_plugin_hook(None, objs)
    space = namespaces[0]
    assert space.mfx.dia.obj1 == obj1
    assert space.mfx.dia.obj2 == obj2
    assert space.mfx.dg2.obj3 == obj3
    assert space.mfx.obj4 == obj4
    assert space.xpp.sb2.obj5 == obj5
