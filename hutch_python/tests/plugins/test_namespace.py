import logging

from hutch_python.plugins.namespace import Plugin


logger = logging.getLogger(__name__)


def test_namespace_plugin_class(assembler):
    logger.debug('test_namespace_plugin_class')
    objs = {'catagory': {'one': 1, 'two': 2.0, 'three': '3'},
            'my_list': ['apples', 4]}
    info = {'class': {'float': ['flt'],
                      'str': ['text', 'words']}}
    plugin = Plugin(info)
    namespaces = plugin.get_objects()
    plugin.future_plugin_hook('something', objs)
    float_space = namespaces['flt']
    assert float_space.two == 2.0
    string_space = namespaces['text']
    assert string_space.three == '3'
    assert string_space.str == 'apples'
    assert string_space == namespaces['words']
