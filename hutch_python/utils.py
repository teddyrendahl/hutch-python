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
    objs: dict
        Mapping from name in file to object
    """
    objs = {}
    # Allow filenames
    module_name = module_name.strip('.py')
    try:
        module = importlib.import_module(module_name)
    except Exception:
        logger.exception('Error loading %s', module_name)
        return objs
    all_kwd = getattr(module, '__all__', None)
    if all_kwd is None:
        all_kwd = [a for a in dir(module) if a[0] != '_']
    for attr in all_kwd:
        obj = getattr(module, attr)
        objs[attr] = obj
    return objs


def assign_names(objs):
    """
    Given a list of objects, either find their name or assign a name based on
    their class.

    Parameters
    ----------
    objs: list of Object

    Returns
    -------
    names: dict
        Mapping of name to object
    """
    name_dict = {}
    for obj in objs:
        name = assign_name(obj)
        name_dict[name] = obj
    return name_dict


def assign_name(obj):
    """
    Find an object's name or assign a name based on the class.

    Parameters
    ----------
    obj: Object

    Returns
    -------
    name: str
    """
    try:
        name = obj.name
    except AttributeError:
        name = type(obj).__name__.lower()
    return name


def find_class(class_path):
    """
    Given a string class name, either return the matching built-in type or
    import the correct module and return the type.

    Parameters
    ----------
    class_path: str
        Built-in type name or import path e.g. ophyd.device.Device

    Returns
    -------
    cls: type
    """
    if '.' in class_path:
        parts = class_path.split('.')
        module_path = '.'.join(parts[:-1])
        class_name = parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    else:
        return eval(class_path)
