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

logger = logging.getLogger(__name__)


def get_happi_objs(db, hutch):
    """
    Get the relevant happi objects for hutch from db.

    Parameters
    ----------
    db: str
        Path to database

    hutch: str
        Name of hutch
    """
    # Load the happi Client
    client = happi.Client(path=db)
    # Assume we want hutch devices that are active
    reqs = dict(beamline=hutch.upper(), active=True)
    containers = client.search(**reqs)
    # Instantiate the devices needed
    dev_namespace = load_devices(*containers, pprint=False)
    return dev_namespace.__dict__
