import os
import logging

import hutch_python.plugins.beamline as bl

logger = logging.getLogger(__name__)


bl.HAPPI_DB = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                           '../happi_db.json')
bl.SIM_DAQ = True


def test_beamline_plugin():
    logger.debug('test_beamline_plugin')
    info = 'tSt'
    plugin = bl.Plugin(info=info)
    pre_plugins = plugin.pre_plugins()
    assert len(pre_plugins) == 1
    pre_plugins[0].get_objects()
    objs = plugin.get_objects()
    assert len(objs) == 2
