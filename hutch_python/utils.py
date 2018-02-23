from contextlib import contextmanager
from functools import partial
from importlib import import_module
from subprocess import check_output
from types import SimpleNamespace
import logging
import sys

import pyfiglet

from .constants import (CUR_EXP_SCRIPT, CLASS_SEARCH_PATH, HUTCH_COLORS,
                        SUCCESS_LEVEL)

logging.addLevelName('SUCCESS', SUCCESS_LEVEL)
logger = logging.getLogger(__name__)
logger.success = partial(logger.log, SUCCESS_LEVEL)


@contextmanager
def safe_load(name, cls=None):
    """
    Context manager to abort running code and resume the rest of the program if
    something fails. This can be used to wrap user code with unknown behavior.
    This will log standard messages to indicate the success state.

    Parameters
    ----------
    name: str
        The name of the load to be logged

    cls: type
        The class of a loaded object to be logged
    """
    if cls is None:
        identifier = name
    else:
        identifier = ' '.join((name, str(cls)))
    logger.info('Loading %s...', identifier)
    try:
        yield
        logger.success('Successfully loaded %s', identifier)
    except Exception as exc:
        logger.error('Failed to load %s', identifier)
        logger.debug(exc, exc_info=True)


def get_current_experiment(hutch):
    """
    Run a script to get the current experiment.
    """
    script = CUR_EXP_SCRIPT.format(hutch)
    return check_output(script)


class IterableNamespace(SimpleNamespace):
    def __iter__(self):
        # Sorts alphabetically by key
        for _, obj in sorted(self.__dict__.items()):
            yield obj

    def __len__(self):
        return len(self.__dict__)


def extract_objs(scope=None, skip_hidden=True, stack_offset=0):
    """
    Return all objects within scope without a _ prefix. If an __all__
    keyword exists, follow that keyword's instructions instead.

    Parameters
    ----------
    scope: module, namespace, or list of these, optional
        If this is omitted, we'll include all objects that have been loaded by
        hutch_python and everything in the caller's global frame.

    skip_hidden: bool, optional
        If changed from True to False, we'll include objects with leading
        underscores.

    stack_offset: int, optional
        If scope was not provided, we'll use stack_offset to determine which
        frame is the user's frame. Leave this at zero if you want the objects
        in the caller's frame, and increase it by one for each level up the
        stack your frame is.

    Returns
    -------
    objs: dict
        Mapping from name in scope to object
    """
    if scope is None:
        stack_depth = 1 + stack_offset
        frame = sys._getframe(stack_depth)
        objs = extract_objs(scope='hutch_python.db',
                            skip_hidden=skip_hidden,
                            stack_offset=stack_offset)
        objs.update(frame.f_globals)
    else:
        if isinstance(scope, list):
            objs = {}
            for s in scope:
                objs.extend(extract_objs(scope=s,
                                         skip_hidden=skip_hidden,
                                         stack_offset=stack_offset))
        else:
            if isinstance(scope, str):
                if scope.endswith('.py'):
                    scope = scope[:-3]
                scope = import_module(scope)
            objs = scope.__dict__.copy()

    all_kwd = getattr(objs, '__all__', None)
    if all_kwd is None:
        if skip_hidden:
            return {k: v for k, v in objs.items() if k[0] != '_'}
        else:
            return objs
    else:
        all_objs = {}
        for kwd in all_kwd:
            all_objs[kwd] = objs.get(kwd)
        return all_objs


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
    module = import_module(module_path)
    return getattr(module, class_name)


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


def strip_prefix(name, strip_text):
    if name.startswith(strip_text):
        return name[len(strip_text)+1:]
    else:
        return name


def hutch_banner(hutch_name='Hutch '):
    text = hutch_name + 'Python'
    f = pyfiglet.Figlet(font='big')
    banner = f.renderText(text)
    if hutch_name in HUTCH_COLORS:
        banner = '\x1b[{}m'.format(HUTCH_COLORS[hutch_name]) + banner
    print(banner)
