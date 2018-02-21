import pcdsdevices.daq as daq_module
import pcdsdevices.sim.pydaq as sim_pydaq

from .constants import DAQ_MAP


def get_daq_objs(hutch, RE, sim=False):
    if sim:
        daq_module.pydaq = sim_pydaq

    daq = daq_module.Daq(platform=DAQ_MAP[hutch], RE=RE)
    return dict(daq=daq, RE=RE)
