import logging
import importlib

logger = logging.getLogger(__name__)


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
    if module_name.endswith('.py'):
        module_name = module_name[:-3]
    elif module_name.endswith('()'):
        module_name = module_name[:-2]
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
    except Exception as exc:
        logger.error('Error loading %s', module_name)
        logger.debug(exc, exc_info=True)
        return objs
    all_kwd = getattr(module, '__all__', None)
    if all_kwd is None:
        all_kwd = [a for a in dir(module) if a[0] != '_']
    for attr in all_kwd:
        obj = getattr(module, attr)
        objs[attr] = obj
    return objs


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


CLASS_SEARCH_PATH = ['pcdsdevices.device_types']


def find_class(class_path, check_defaults=True):
    """
    Given a string class name, either return the matching built-in type or
    import the correct module and return the type.

    Parameters
    ----------
    class_path: str
        Built-in type name or import path e.g. ophyd.device.Device

    check_defaults: bool
        If True, try checking for context for each module in CLASS_SEARCH_PATH

    Returns
    -------
    cls: type
    """
    try:
        if '.' in class_path:
            return find_object(class_path)
        else:
            return eval(class_path)
    except NameError:
        if check_defaults:
            for default in CLASS_SEARCH_PATH:
                try:
                    return find_class(default + '.' + class_path,
                                      check_defaults=False)
                except NameError:
                    pass
        raise
