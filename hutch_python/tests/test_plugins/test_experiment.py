import logging

import pytest

import hutch_python.plugins.questionnaire
from hutch_python.plugins.experiment import Plugin

from ..conftest import QSBackend

logger = logging.getLogger(__name__)


def test_experiment_plugin():
    logger.debug('test_experiment_plugin')

    info = {'name': 'sample_expname',
            'import': 'experiment'}
    conf = dict(experiment=info)
    plugin = Plugin(conf)
    objs = plugin.get_objects()
    assert 'sample_plan' in objs
    assert 'another' in objs

    info = {'name': 'sample_expname',
            'import': 'experiment.sample_plan'}
    conf = dict(experiment=info)
    plugin = Plugin(conf)
    objs = plugin.get_objects()
    assert 'sample_plan' in objs
    assert 'another' not in objs

    info = {'name': 'sample_expname',
            'import': 'experiment.sample_plan()'}
    conf = dict(experiment=info)
    plugin = Plugin(conf)
    objs = plugin.get_objects()
    assert objs['sample_plan'] == 5

    info = {'name': 'sample_expname',
            'import': 'experiment as x'}
    conf = dict(experiment=info)
    plugin = Plugin(conf)
    objs = plugin.get_objects()
    assert 'x' in objs

    info = {'name': 'sample_expname',
            'import': 'experiment.sample_plan as x, y'}
    conf = dict(experiment=info)
    plugin = Plugin(conf)
    objs = plugin.get_objects()
    assert 'x' in objs
    assert 'y' in objs


def test_experiment_auto():
    logger.debug('test_experiment_auto')

    info = {'name': 'automatic',
            'import': 'experiment'}
    conf = dict(experiment=info)
    plugin = Plugin(conf)
    with pytest.raises(NotImplementedError):
        plugin.get_objects()


def test_questionnaire_preplugin():
    info = {'run': 15, 'proposal': 'LR12'}
    conf = dict(experiment=info)
    plugin = Plugin(conf)
    hutch_python.plugins.questionnaire.QSBackend = QSBackend
    pre_plugins = plugin.pre_plugins()
    objs = pre_plugins[0].get_objects()
    assert objs['inj_x'].run == '15'
    assert objs['inj_x'].proposal == 'LR12'
