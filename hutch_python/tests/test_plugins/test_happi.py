import os.path
import logging

from hutch_python.plugins.happi import Plugin

logger = logging.getLogger(__name__)


def test_happi_plugin():
    _db = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       '../happi_db.json')
    logger.debug("test_happi_plugin")
    # Select all the available objects
    info = {'filename': _db}
    conf = dict(happi=info)
    plugin = Plugin(conf)
    objs = plugin.get_objects()
    assert len(objs) == 3
    # Only select active objects
    info = {'filename': _db,
            'requirements': {'active': True}}
    conf = dict(happi=info)
    plugin = Plugin(conf)
    objs = plugin.get_objects()
    assert len(objs) == 2
    assert all([obj.active for obj in objs.values()])
