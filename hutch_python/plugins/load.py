import logging

from ..base_plugin import BasePlugin
from .. import utils

logger = logging.getLogger(__name__)


class Plugin(BasePlugin):
    """
    Plugin to load arbitrary files for generic hutch-specific includes.
    """
    name = 'load'

    def get_objects(self):
        objs = {}
        for filename in self.info:
            logger.info('Loading %s', filename)
            module_objs = utils.extract_objs(filename)
            objs.update(module_objs)
        return objs
