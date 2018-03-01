import logging
from importlib import import_module

import pcdsdevices.daq as daq_module
import pcdsdevices.sim.pydaq as sim_pydaq

from .constants import DAQ_MAP

logger = logging.getLogger(__name__)


def get_daq_objs(hutch, RE):
    daq = daq_module.Daq(platform=DAQ_MAP[hutch], RE=RE)
    return dict(daq=daq, RE=RE)


def set_daq_sim(sim):
    if sim:
        daq_module.pydaq = sim_pydaq
    else:
        try:
            pydaq = import_module('pydaq')
            daq_module.pydaq = pydaq
        except ImportError:
            logger.error('Cannot disable daq sim, pydaq unavailable')
