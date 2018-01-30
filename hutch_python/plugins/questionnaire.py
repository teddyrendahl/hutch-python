"""
This plugin depends on the QSBackend in `happi`. Not intended to be run
individually, it is expected that the requisite information is passed in the
`experiment` section. This includes the proposal id and run.

A connection to the Questionnaire webservice is made and the devices that have
enough information to be turned into Python objects are instantiated.
"""
import logging

import happi
from happi.loader import load_devices
from happi.backends.qs_db import QSBackend

from ..base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class Plugin(BasePlugin):
    """
    Plugin to load information from the LCLS Questionnaire
    """
    name = 'questionnaire'

    def get_objects(self):
        run = self.conf['experiment'].get('run')
        proposal = self.conf['experiment'].get('proposal')
        if run and proposal:
            logger.debug("Loading Questionnaire information for %s in Run %s",
                         proposal, run)
            qs_client = happi.Client(database=QSBackend(run, proposal))
        else:
            raise ValueError("Inadequate information to load Questionnaire. "
                             "Must specify proposal and run.")
        dev_namespace = load_devices(*qs_client.all_devices, pprint=True)
        return dev_namespace.__dict__
