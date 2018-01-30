"""
This plugin depends on a JSON happi database stored somewhere in the file
system. The path of this file is supplied in the YAML as ``filename``.
Finally, if a smaller subsection of the databse is desired, a requirements
specification can be used to limit the number of devices that are loaded.

The plugin then handles; initalizing the ``happi.Client``, finding the
containers that match the specified requirements, then using the device
loading utilities from happi to create instantiated devices

Example
-------
.. code:: YAML

    happi:
        filename: path/to/my_db.json
        requirements:
            active: True
            beamline: MFX
"""
import logging

import happi
from happi.loader import load_devices

from ..base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class Plugin(BasePlugin):
    """
    Plugin to load search information from happi
    """
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
        dev_namespace = load_devices(*containers, pprint=False)
        return dev_namespace.__dict__
