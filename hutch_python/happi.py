"""
This plugin depends on a JSON happi database stored somewhere in the file
system. The path of this file is supplied in the YAML as ``filename``.
Finally, if a smaller subsection of the databse is desired, a requirements
specification can be used to limit the number of devices that are loaded.

The plugin then handles; initalizing the ``happi.Client``, finding the
containers that match the specified requirements, then using the device
loading utilities from happi to create instantiated devices. The same database
information can be used to create a `lightpath.BeamPath` object that provides a
convenient way to visualize all the devices that may block the beam on the way
to the interaction point.

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
import lightpath
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
    if not containers:
        logger.warning("No devices found in database for %s",
                       hutch.upper())
        return dict()
    # Instantiate the devices needed
    dev_namespace = load_devices(*containers, pprint=False)
    return dev_namespace.__dict__


def get_lightpath(db, hutch):
    """
    Create a lightpath from relevant happi objects

    Parameters
    ----------
    db: str
        Path to database

    hutch: str
        Name of hutch
    """
    # Load the happi Client
    client = happi.Client(path=db)
    # Allow the lightpath module to create a path
    lc = lightpath.LightController(client, endstations=[hutch.upper()])
    # Return the BeamPath object created by the LightController
    return lc.beamlines[hutch.upper()]
