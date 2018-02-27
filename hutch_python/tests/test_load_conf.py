import logging
import os.path

from hutch_python.load_conf import load, load_conf

logger = logging.getLogger(__name__)


def test_file_load():
    logger.debug('test_file_load')
    objs = load(os.path.join(os.path.dirname(__file__), 'conf.yaml'))
    should_have = ('x', 'unique_device', 'calc_thing')
    for elem in should_have:
        assert elem in objs


def test_no_file():
    logger.debug('test_no_file')
    objs = load()
    assert len(objs) > 1


def test_conf_empty():
    logger.debug('test_conf_empty')
    objs = load_conf({})
    assert len(objs) > 1


def test_skip_failures():
    logger.debug('test_skip_failures')
    # Should not raise
    load_conf(dict(hutch=345243, db=12351324, experiment=2341234, load=123454,
                   bananas='dole'))
