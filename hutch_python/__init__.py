import logging
from types import SimpleNamespace
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions
logger = logging.getLogger(__name__)


def register_load(plugin_name, objs):
    """
    Add a user-accessible namespace. You can refer to these in later plugin
    load stages, or interactively if desired. These take the form of objects
    like `hutch_python.questionnaire` that can be imported and contain the
    loaded objects like `hutch_python.questionnaire.sam_x`.
    """
    plugin_loads.append(plugin_name)
    namespace = globals().get(plugin_name)
    if namespace is None:
        globals()[plugin_name] = SimpleNamespace(**objs)
    else:
        namespace.__dict__.update(objs)


def clear_load():
    """
    Clear the user-accessible namespaces. This is called every time we call
    read_conf to make sure we don't have objects from previous loads.
    """
    logger.debug('Clearing hutch_python plugins cache')
    for plugin in plugin_loads:
        del globals()[plugin]
    globals()['plugin_loads'] = []


plugin_loads = []
