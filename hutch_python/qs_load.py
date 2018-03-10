import logging
import os.path
from configparser import NoOptionError, ConfigParser

import happi
from happi.loader import load_devices
from happi.backends.qs_db import QSBackend

from .utils import safe_load

logger = logging.getLogger(__name__)


def get_qs_objs(proposal, run):
    """
    Gather user objects from the experiment questionnaire.

    Connects to the questionnaire webservice via the ``happi`` ``QSBackend``
    using ``psdm_qs_cli`` to collect well-defined devices.

    There are two possible methods of authentication to the
    ``QuestionnaireClient``, ``Kerberos`` and ``WS-Auth``. The first is simpler
    but is not possible for all users, we therefore search for a configuration
    file named ``qs.cfg``, either hidden in the current directory or the users
    home directory. This should contain the username and password needed to
    authenticate into the ``QuestionnaireClient``. The format of this
    configuration file is the standard ``.ini`` structure and should define the
    username and password like:

    .. code::

        [DEFAULT]
        user = MY_USERNAME
        pw = MY_PASSWORD

    Parameters
    ----------
    proposal: ``str``
        The experiment's proposal number

    run: ``str``
        A string representation of the run number

    Returns
    -------
    objs: ``dict``
        Mapping from questionnaire ``python name`` to loaded object.
    """
    logger.debug('get_qs_objs(%s, %s)', proposal, run)
    with safe_load('questionnaire'):
        proposal = proposal.upper()
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

        dev_namespace = load_devices(*qs_client.all_devices, pprint=False)
        return dev_namespace.__dict__
    return {}
