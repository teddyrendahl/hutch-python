import logging
from types import SimpleNamespace
from ._version import get_versions

__version__ = get_versions()['version']
del get_versions
logger = logging.getLogger(__name__)


def clear_load():
    """
    Create a new user-accessible namespace for the current load. This is called
    once at module __init__ and will be called again every time we call
    read_conf to make sure we don't have objects from previous loads.
    """
    logger.debug('Clearing hutch_python.objects cache')
    globals()['objects'] = SimpleNamespace()


clear_load()
