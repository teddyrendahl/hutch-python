import logging
import importlib

logger = logging.getLogger(__name__)


def interpret_list(info):
    """
    Intepret a yaml segment like:
    stuff:
        - thing
        - thing
    or
    stuff:
        thing
        thing
    as ['thing', 'thing']

    Parameters
    ----------
    info: str or list of str
        This is the value from the dictionaries generated from the above yaml
        files. The first will look like ['thing', 'thing'], but the second will
        look like 'thing thing'.

    Returns
    -------
    elems: list of str
    """
    if isinstance(info, str):
        elems = info.split(' ')
    elif isinstance(info, list):
        elems = info
    else:
        raise RuntimeError('Malformed config')
    return elems


def extract_objs(module_name):
    """
    Import module and return all the objects without a _ prefix. If an __all__
    keyword exists, follow that keyword's instructions instead.

    Parameters
    ----------
    module_name: str
        Filename or module name

    Returns
    -------
    objs: list of Objects
    """
    objs = []
    # Allow filenames
    module_name = module_name.strip('.py')
    try:
        module = importlib.import_module(module_name)
    except Exception:
        logger.exception('Error loading %s', module_name)
        return objs
    all_kwd = getattr(module, '__all__', None)
    if all_kwd is None:
        all_kwd = (a for a in dir(module) if a[0] != '_')
    for name in all_kwd:
        try:
            obj = module.name
            objs.append(obj)
        except AttributeError:
            pass
    return objs
