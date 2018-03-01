import logging

from hutch_python.exp_load import get_exp_objs

logger = logging.getLogger(__name__)


def test_experiment_objs():
    logger.debug('test_experiment_objs')

    objs = get_exp_objs('sample', '_expname')
    assert 'x' in objs

    empty = get_exp_objs('q3qwer', '13241234')
    assert len(empty) == 0
