import logging

from hutch_python.plugins.load import Plugin

logger = logging.getLogger(__name__)


def test_load_plugin():
    logger.debug('test_load_plugin')
    # Test basic import
    info = {'import': 'sample_module_1'}
    conf = dict(load=info)
    plugin = Plugin(conf)
    objs = plugin.get_objects()
    assert objs['hey'] == '4horses'
    assert objs['milk'] == 'cows'
    assert objs['some_int'] == 5
    # Test renaming import
    info['import'] = 'sample_module_2 as x'
    plugin = Plugin(conf)
    objs = plugin.get_objects()
    assert objs['x'] == 5.0
    # Test selective import
    info['import'] = 'sample_module_1.some_func'
    plugin = Plugin(conf)
    objs = plugin.get_objects()
    assert 'some_func' in objs
    assert 'hey' not in objs
    # Test function return import
    info['import'] = 'sample_module_1.some_func()'
    plugin = Plugin(conf)
    objs = plugin.get_objects()
    assert objs['some_func'] == 4
    # Test double rename
    info['import'] = 'sample_module_1.hey as x, y'
    plugin = Plugin(conf)
    objs = plugin.get_objects()
    assert 'x' in objs
    assert 'y' in objs
