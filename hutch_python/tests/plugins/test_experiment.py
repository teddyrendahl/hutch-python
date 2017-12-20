import logging

from hutch_python.yaml_experiment import load_objs

logger = logging.getLogger(__name__)


def test_load_experiment():
    logger.debug('test_load_experiment')
    info = ['sample_expname']
    objs = load_objs(info)
    assert 'sample_plan' in objs
    assert 'another' in objs
    info = ['sample_expname.sample_plan']
    objs = load_objs(info)
    assert 'sample_plan' in objs
    assert 'another' not in objs
    info = ['sample_expname.sample_plan()']
    objs = load_objs(info)
    assert objs['sample_plan'] == 5
