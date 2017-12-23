import logging

from hutch_python.base_plugin import BasePlugin

logger = logging.getLogger(__name__)


def test_base_plugin():
    logger.debug('test_base_plugin')
    plugin = BasePlugin({})
    plugin.get_objects()
    plugin.future_object_hook('name', 'obj')
    plugin.future_plugin_hook('source', {})
