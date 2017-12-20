import logging

from hutch_python.plugins.experiment import Plugin

logger = logging.getLogger(__name__)


def test_experiment_plugin():
    logger.debug('test_experiment_plugin')

    info = {'name': 'sample_expname',
            'import': 'experiment'}
    plugin = Plugin(info)
    objs = plugin.get_objects()
    assert 'sample_plan' in objs
    assert 'another' in objs

    info = {'name': 'sample_expname',
            'import': 'experiment.sample_plan'}
    plugin = Plugin(info)
    objs = plugin.get_objects()
    assert 'sample_plan' in objs
    assert 'another' not in objs

    info = {'name': 'sample_expname',
            'import': 'experiment.sample_plan()'}
    plugin = Plugin(info)
    objs = plugin.get_objects()
    assert objs['sample_plan'] == 5

    info = {'name': 'sample_expname',
            'import': 'experiment as x'}
    plugin = Plugin(info)
    objs = plugin.get_objects()
    assert 'x' in objs

    info = {'name': 'sample_expname',
            'import': 'experiment.sample_plan as x, y'}
    plugin = Plugin(info)
    objs = plugin.get_objects()
    assert 'x' in objs
    assert 'y' in objs
