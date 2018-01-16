import logging

import happi
from happi.loader import load_devices

from ..base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class Plugin(BasePlugin):
    """
    Plugin to load search information from happi
    """
    priority = 5
    name = 'happi'

    def get_objects(self):
        # Load the happi Client. Use the configured kwargs to find the
        # containers requested, and then instantiate the devices needed
        _file = self.info['filename']
        client = happi.Client(path=_file)
        # If we have no requirements, we want all the devices. Otherwise use
        # the listed requirements dictionary
        reqs = self.info.get('requirements', {})
        if not reqs:
            containers = client.all_devices
        else:
            containers = client.search(**reqs)
        dev_namespace = load_devices(*containers, pprint=True)
        return dev_namespace.__dict__
