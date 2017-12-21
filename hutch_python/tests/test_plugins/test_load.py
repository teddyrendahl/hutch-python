import logging

from hutch_python.plugins.load import Plugin

logger = logging.getLogger(__name__)


def test_load_plugin():
    logger.debug('test_load_plugin')
    info = ['sample_module_1', 'sample_module_2.py']
    plugin = Plugin(info)
    objs = plugin.get_objects()
    assert objs['hey'] == '4horses'
    assert objs['milk'] == 'cows'
    assert objs['some_int'] == 5
    assert objs['just_this'] == 5.0
