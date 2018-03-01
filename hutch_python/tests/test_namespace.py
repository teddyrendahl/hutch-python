import logging
from types import SimpleNamespace

from hutch_python.namespace import class_namespace, metadata_namespace


logger = logging.getLogger(__name__)


def test_class_namespace():
    logger.debug('test_class_namespace')
    scope = SimpleNamespace(one=1, two=2.0, three='3', four=lambda x: 4)
    int_space = class_namespace(int, scope)
    float_space = class_namespace(float, scope)
    str_space = class_namespace(str, scope)
    func_space = class_namespace('function', scope)
    err_space = class_namespace('erqwerasd', scope)
    assert int_space.one == 1
    assert float_space.two == 2.0
    assert str_space.three == '3'
    assert func_space.four(1) == 4
    assert len(err_space) == 0


def test_metadata_namespace():
    logger.debug('test_metadata_namespace')
    obj1 = SimpleNamespace()
    obj2 = SimpleNamespace()
    obj3 = SimpleNamespace()
    obj4 = SimpleNamespace()
    obj5 = SimpleNamespace()
    obj6 = SimpleNamespace()
    obj1.md = SimpleNamespace(beamline='MFX', stand='DIA')
    obj2.md = SimpleNamespace(beamline='MFX', stand='DIA')
    obj3.md = SimpleNamespace(beamline='MFX', stand='DG2')
    obj4.md = SimpleNamespace(beamline='MFX')
    obj5.md = SimpleNamespace(beamline='XPP', stand='SB2')
    obj6.md = SimpleNamespace(beamline='MFX', stand='DIA')
    scope = SimpleNamespace(mfx_dia_obj1=obj1, mfx_dia_obj2=obj2,
                            mfx_dg2_obj3=obj3, mfx_obj4=obj4,
                            xpp_sb2_obj5=obj5, hello=obj6)
    md = ['beamline', 'stand']
    namespaces = metadata_namespace(md, scope=scope)
    mfx = namespaces.mfx
    xpp = namespaces.xpp
    assert mfx.dia.obj1 == obj1
    assert mfx.dia.obj2 == obj2
    assert mfx.dg2.obj3 == obj3
    assert mfx.obj4 == obj4
    assert xpp.sb2.obj5 == obj5
    assert mfx.dia.hello == obj6


def test_metadata_namespace_fallback():
    logger.debug('test_metadata_namespace_fallback')
    # objects without md, so use name
    obj1 = SimpleNamespace()
    obj2 = SimpleNamespace()
    obj3 = SimpleNamespace()
    scope = SimpleNamespace(mfx_dia_obj1=obj1, mfx_dia_obj2=obj2,
                            mfx_dg2_obj3=obj3)
    md = ['beamline', 'stand']
    namespaces = metadata_namespace(md, scope=scope)
    mfx = namespaces.mfx
    assert mfx.dia.obj1 == obj1
    assert mfx.dia.obj2 == obj2
    assert mfx.dg2.obj3 == obj3
