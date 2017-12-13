import logging

from hutch_python.yaml_experiment import load_objs

logger = logging.getLogger(__name__)


def test_load_experiment():
    logger.debug('test_load_experiment')
    info = ['sample_expname']
    objs = load_objs(info)
    assert 'sample_plan' in objs
