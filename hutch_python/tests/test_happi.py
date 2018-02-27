import os.path
import logging

from hutch_python.happi import get_happi_objs

logger = logging.getLogger(__name__)


def test_happi_objs():
    logger.debug("test_happi_objs")
    db = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                      'happi_db.json')
    # Only select active objects
    objs = get_happi_objs(db, 'tst')
    assert len(objs) == 2
    assert all([obj.active for obj in objs.values()])
