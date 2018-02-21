import logging

from .utils import safe_load, extract_objs

logger = logging.getLogger(__name__)


def get_user_objs(load):
    """
    Load the user's modules. Each of these modules will be imported and the
    objects that they define will make it into the final namespace.

    Parameters
    ----------
    load: str or list of str
        The modules to import
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
