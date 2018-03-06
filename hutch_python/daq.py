import logging

from pcdsdaq.daq import Daq

from .constants import DAQ_MAP

logger = logging.getLogger(__name__)


def get_daq_objs(hutch, RE):
    daq = Daq(platform=DAQ_MAP[hutch], RE=RE)
    return dict(daq=daq, RE=RE)
