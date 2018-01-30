import logging
import os.path

from hutch_python.base_plugin import BasePlugin
from hutch_python.load_conf import load, read_conf, run_plugins

logger = logging.getLogger(__name__)


def test_load_normal():
    logger.debug('test_load_normal')
    objs = load(os.path.join(os.path.dirname(__file__), 'conf.yaml'))
    should_have = ('x', 'fn', 'funcs', 'unique_device', 'calc_thing')
    for elem in should_have:
        assert elem in objs
    assert len(objs['funcs'].__dict__) == 1
    assert objs['fn'] == objs['funcs']


def test_read_empty():
    logger.debug('test_read_empty')
    objs = read_conf({})
    assert objs == {}


def test_read_duplicate():
    logger.debug('test_read_duplicate')
    objs = read_conf({'load': ['sample_module_1.py', 'sample_module_1.py']})
    assert len(objs) == 4


def test_read_only_namespaces():
    logger.debug('test_read_only_namespaces')
    objs = read_conf({'namespace': {'class': {'float': ['text', 'words']}}})
    assert len(objs) == 2


def test_ignores_bad_plugin():
    logger.debug('test_ignores_bad_plugin')
    objs = read_conf({'awoeifdhasd': True})


class BadGetObjects(BasePlugin):
    name = 'broken'

    def get_objects(self):
        raise RuntimeError('I am broken for the test')


class SimplePlugin(BasePlugin):
    name = 'simple'

    def get_objects(self):
        return {'name': 'text'}


class BadFutureHook(SimplePlugin):
    name = 'broken'

    def future_plugin_hook(self, *args, **kwargs):
        raise RuntimeError('I am broken for the test')


def test_skip_failures():
    logger.debug('test_skip_failures')
    conf = dict(broken={}, simple={})
    bad_plugins = {0: [BadGetObjects(conf),
                       BadFutureHook(conf),
                       SimplePlugin(conf)]}
    objs = run_plugins(bad_plugins)
    assert objs['name'] == 'text'
