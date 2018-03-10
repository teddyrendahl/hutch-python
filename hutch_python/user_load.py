import logging

from .utils import safe_load, extract_objs

logger = logging.getLogger(__name__)


def get_user_objs(load):
    """
    Load the user's modules.

    All objects from these modules will be imported e.g.
    ``from module import *`` and the objects will be returned.

    Parameters
    ----------
    load: ``str`` or ``list`` of ``str``
        The modules to import

    Returns
    -------
    objs: ``dict``
        Mapping from object name to object
    """
    if isinstance(load, str):
        return get_user_objs([load])
    else:
        objs = {}
        for module in load:
            with safe_load(module):
                module_objs = extract_objs(module)
                objs.update(module_objs)
        return objs
