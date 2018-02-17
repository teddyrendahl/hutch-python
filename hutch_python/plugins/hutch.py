import pcdsdevices.daq as daq_module
import pcdsdevices.sim.pydaq as sim_pydaq
from pcdsdevices.daq import Daq, calib_cycle, daq_wrapper, daq_decorator

from bluesky import RunEngine

from ..base_plugin import BasePlugin
from .happi import Plugin as HappiPlugin

DAQ_MAP = dict(mfx=4,
               tst=0)
HAPPI_DB = 'filename add here later'
SIM_DAQ = False


class Plugin(BasePlugin):
    name = 'hutch'

    def pre_plugins(self):
        requirements = dict(active=True,
                            beamline=self.info.upper())
        info = dict(filename=HAPPI_DB,
                    requirements=requirements)
        return [HappiPlugin(info=info)]

    def get_objects(self):
        if SIM_DAQ:
            daq_module.pydaq = sim_pydaq
        hutch = self.info.lower()
        RE = RunEngine({})
        daq = Daq(platform=DAQ_MAP[hutch], RE=RE)
        return dict(daq=daq, RE=RE, calib_cycle=calib_cycle,
                    daq_wrapper=daq_wrapper, daq_decorator=daq_decorator)
