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

    If this is a single object in a module rather than a module, import just
    that object.

    If this is a callable and it ends in (), call it and import the return
    value. Note that this includes classes.

    Parameters
    ----------
    module_name: str
        Filename, module name, or path to object in module

    Returns
    -------
    objs: dict
        Mapping from name in file to object
    """
    objs = {}
    # Allow filenames
    module_name = module_name.strip('.py')
    if '()' in module_name:
        module_name.strip('()')
        call_me = True
    else:
        call_me = False
    try:
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            my_obj = find_object(module_name)
            name = module_name.split('.')[-1]
            # call_me, maybe
            if call_me:
                objs[name] = my_obj()
            else:
                objs[name] = my_obj
            return objs
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


def find_object(obj_path):
    """
    Given a string module path to an object, return that object.

    Parameters
    ----------
    obj_path: str
        String module path to an object

    Returns
    -------
    obj: Object
        That object
    """
    parts = obj_path.split('.')
    module_path = '.'.join(parts[:-1])
    class_name = parts[-1]
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


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
        return find_object(class_path)
    else:
        return eval(class_path)
