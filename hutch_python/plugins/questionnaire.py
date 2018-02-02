"""
This plugin depends on the QSBackend in `happi`. Not intended to be run
individually, it is expected that the requisite information is passed in the
`experiment` section. This includes the proposal id and run.

A connection to the Questionnaire webservice is made and the devices that have
enough information to be turned into Python objects are instantiated. There are
two possible methods of authentication to the QuestionnaireClient, Kerberos and
WS-Auth. The first is simpler but is not possible for all users, we therefore
search for a configuration file named `qs.cfg`, either hidden in the current
directory or the users home directory. This should contain the user and
password needed to authenticate into the QuestionnaireClient. The format of
this configuration file is the standard .ini structure and should define the
username and password like:

.. code::

    [DEFAULT]
    user = MY_USERNAME
    pw = MY_PASSWORD


"""
import logging
import os.path
from configparser import NoOptionError, ConfigParser

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
            # Determine which method of authentication we are going to use.
            # Search for a configuration file, either in the current directory
            # or hidden in the users home directory. If not found, attempt to
            # launch the client via Kerberos
            cfg = ConfigParser()
            cfgs = cfg.read(['qs.cfg', '.qs.cfg',
                             os.path.expanduser('~/.qs.cfg')])
            # Ws-auth
            if cfgs:
                user = cfg.get('DEFAULT', 'user', fallback=None)
                try:
                    pw = cfg.get('DEFAULT', 'pw')
                except NoOptionError as exc:
                    raise ValueError("Must specify password as 'pw' in "
                                     "configuration file") from exc
                qs_client = happi.Client(database=QSBackend(run, proposal,
                                                            use_kerberos=False,
                                                            user=user, pw=pw))
            # Kerberos
            else:
                qs_client = happi.Client(database=QSBackend(run, proposal,
                                                            use_kerberos=True))

        else:
            raise ValueError("Inadequate information to load Questionnaire. "
                             "Must specify proposal and run.")
        dev_namespace = load_devices(*qs_client.all_devices, pprint=False)
        return dev_namespace.__dict__
