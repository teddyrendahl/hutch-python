import logging

from pcdsdaq.daq import Daq

logger = logging.getLogger(__name__)


def get_daq_objs(platform, RE):
    """
    Create an instance of ``Daq``.

    This makes sure that the ``Daq`` object is set up to connect to a
    hutch's daq, and that it is ready to use in scans with ``RE``.

    Parameters
    ----------
    platform: ``int``
        The daq platform variable associated with the hutch's daq.

    RE: ``RunEngine``
        The session's ``RE`` object

    Returns
    -------
    objs: ``dict``
        A dictionary that contains a single key, ``daq``, and a ready instance
        of the ``Daq`` class.
    """
    daq = Daq(platform=platform, RE=RE)
    return dict(daq=daq)
