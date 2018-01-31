from pcdsdevices.daq import Daq, make_daq_run_engine
from pcdsdevices.sim.daq import SimDaq

from ..base_plugin import BasePlugin
from .happi import Plugin as HappiPlugin

DAQ_MAP = dict(mfx=4,
               tst=0)
HAPPI_DB = 'filename add here later'
SIM_DAQ = False


class Plugin(BasePlugin):
    name = 'beamline'

    def pre_plugins(self):
        requirements = dict(active=True,
                            beamline=self.info.upper())
        info = dict(filename=HAPPI_DB,
                    requirements=requirements)
        return [HappiPlugin(info=info)]

    def get_objects(self):
        # Make the Daq object
        hutch = self.info.lower()
        if SIM_DAQ:
            Cls = SimDaq
        else:
            Cls = Daq
        daq = Cls(name='daq', platform=DAQ_MAP[hutch])
        # Make the Daq RunEngine
        RE = make_daq_run_engine(daq)
        return dict(daq=daq, RE=RE)
