import os.path
import logging

from hutch_python.happi import get_happi_objs, get_lightpath

logger = logging.getLogger(__name__)


def test_happi_objs():
    logger.debug("test_happi_objs")
    db = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                      'happi_db.json')
    # Only select active objects
    objs = get_happi_objs(db, 'tst')
    assert len(objs) == 2
    assert all([obj.active for obj in objs.values()])


def test_get_lightpath():
    logger.debug("test_get_lightpath")
    db = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                      'happi_db.json')
    obj = get_lightpath(db, 'tst')
    # Check that we created a valid BeamPath with no inactive objects
    assert obj.name == 'TST'
    assert len(obj.devices) == 2
