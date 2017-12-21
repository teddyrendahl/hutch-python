import logging
import yaml
from importlib import import_module
from collections import defaultdict

import hutch_python

logger = logging.getLogger(__name__)


def load(filename):
    """
    Load the hutch-specific conf.yml file.

    Parameters
    ----------
    filename: str
        Path the conf.yml file

    Returns
    -------
    objs: dict{str: Object}
        All objects defined by the file that need to make it into the
        environment. The strings are the names that will be accessible in the
        global namespace.
    """
    with open(filename, 'r') as f:
        conf = yaml.load(f)
    return read_conf(conf)


def read_conf(conf):
    """
    Separate this from load to make it easier to test without tons of temp
    files.

    Parameters
    ----------
    conf: dict
        dict interpretation of the original yaml file
    """
    hutch_python.clear_load()
    all_objects = hutch_python.objects
    plugins = defaultdict(list)

    for plugin_name, info in conf.items():
        try:
            module = import_module('hutch_python.plugins.' + plugin_name)
        except ImportError as exc:
            module = None
            err = 'Plugin {} is not available, skipping'
            logger.warning(err.format(plugin_name))
            logger.debug(exc, exc_info=True)
            continue
        this_plugin = module.Plugin(info)
        plugins[this_plugin.priority].append(this_plugin)

    plugin_priorities = reversed(sorted(list(plugins.keys())))
    executed_plugins = []

    for prio in plugin_priorities:
        for this_plugin in plugins[prio]:
            try:
                objs = this_plugin.get_objects()
            except Exception as exc:
                objs = None
                err = 'Plugin {} failed to load, skipping'
                logger.error(err.format(this_plugin.name))
                logger.debug(exc, exc_info=True)
                continue
            for past_plugin in executed_plugins:
                try:
                    past_plugin.future_plugin_hook(this_plugin.name, objs)
                except Exception as exc:
                    err = 'Plugin {} post-hook failed for plugin {}'
                    logger.error(err.format(past_plugin.name,
                                            this_plugin.name))
                    logger.debug(exc, exc_info=True)
            executed_plugins.append(this_plugin)
            all_objects.__dict__.update(objs)

    return all_objects.__dict__
