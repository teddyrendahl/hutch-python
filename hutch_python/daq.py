import logging

from pcdsdaq.daq import Daq

from .constants import DAQ_MAP

logger = logging.getLogger(__name__)


def get_daq_objs(hutch, RE):
    """
    Create an instance of ``Daq`` for ``hutch``.

    This makes sure that the ``Daq`` object is set up to connect to that
    hutch's daq, and that it is ready to use in scans with ``RE``.

    Parameters
    ----------
    hutch: ``str``
        The relevant hutch name

    RE: ``RunEngine``
        The session's ``RE`` object

    Returns
    -------
    objs: ``dict``
        A dictionary that contains a single key, ``daq``, and a ready instance
        of the ``Daq`` class.
    """
    daq = Daq(platform=DAQ_MAP[hutch], RE=RE)
    return dict(daq=daq)
