from collections import defaultdict
from importlib import import_module
import inspect
import logging
import sys

from .utils import IterableNamespace, find_class, strip_prefix

logger = logging.getLogger(__name__)


def class_namespace(cls, scope=None):
    """
    Create a namespace that contains objects of a specific type.

    Parameters
    ----------
    cls: type

    scope: module, namespace, or list of these
        Every object attached to the given modules will be considered for the
        class_namespace. If scope is omitted, we'll check all objects loaded by
        hutch_python and everything in the caller's global frame.

    Returns
    -------
    namespace: IterableNamespace
    """
    class_objs = defaultdict(IterableNamespace)
    for cls_name, space_names in opts.items():
        try:
            if cls_name == 'function':
                cls = 'function'
            else:
                cls = find_class(cls_name)
        except Exception as exc:
            cls = None
            err = 'Type {} could not be loaded'
            logger.error(err.format(cls_name))
            logger.debug(exc, exc_info=True)
            continue
        for ns_name in space_names:
            namespace = class_objs[ns_name]
            logger.debug('Added class namespace for type %s as name %s',
                         cls, ns_name)
            for name, obj in prev_objs.items():
                ok = False
                if cls == 'function':
                    if inspect.isfunction(obj):
                        ok = True
                elif isinstance(obj, cls):
                    ok = True
                if ok:
                    setattr(namespace, name, obj)
                    logger.debug('Add %s to namespace %s', name, ns_name)
    return class_objs


def metadata_namespace(md, scope=None):
    """
    Create a namespace that accumulates objects and creates a tree based on
    their metadata.

    Parameters
    ----------
    md: list of str
        Each of the metadata categories to group objects by, in order from the
        root of the tree to the leaves.

    scope: module, namespace, or list of these
        Every object attached to the given modules will be considered for the
        metadata_namespace. If scope is omitted, we'll check all objects loaded
        by hutch_python and everything in the caller's global frame.

    Returns
    -------
    namespace: IterableNamespace
    """
    metadata_objs = defaultdict(IterableNamespace)
    for name, obj in prev_objs.items():
        if hasattr(obj, 'md'):
            raw_keys = [getattr(obj.md, filt, None) for filt in opts]
            keys = []
            for key in raw_keys:
                if isinstance(key, str):
                    keys.append(key.lower())
                else:
                    keys.append(key)
            if keys[0] is None:
                continue
            else:
                upper_space = metadata_objs[keys[0]]
            logger.debug('Add %s to namespace metadata', name)
            name = self.strip_prefix(name, keys[0])
            for key in keys[1:]:
                if key is None:
                    break
                name = self.strip_prefix(name, key)
                if not hasattr(upper_space, key):
                    setattr(upper_space, key, IterableNamespace())
                upper_space = getattr(upper_space, key)
            setattr(upper_space, name, obj)
    return metadata_objs


def get_all_objects(scope=None, stack_offset=0):
    """
    Get all of the objects that fall within the scope.

    Parameters
    ----------
    scope: module, namespace, or list of these, optional
        If this is omitted, we'll include all objects that have been loaded by
        hutch_python and everything in the caller's global frame.

    stack_offset: int, optional
        If scope was not provided, we'll use stack_offset to determine which
        frame is the user's frame. Leave this at zero if you want the objects
        in the caller's frame, and increase it by one for each level up the
        stack your frame is.

    Returns
    -------
    objs: dict
    """
    if scope is None:
        stack_depth = 1 + stack_offset
        frame = sys._getframe(stack_depth)
        objs = get_all_objects(scope='hutch_python.db')
        objs.update(frame.f_globals)
        return objs
    else:
        if isinstance(scope, list):
            objs = {}
            for s in scope:
                objs.extend(get_all_objects(scope=s))
            return objs
        else:
            if isinstance(scope, str):
                try:
                    scope = import_module(scope)
                except ImportError:
                    logger.debug('Cannot get_all_objects from %s', scope,
                                 exc_info=True)
                    return {}
            return scope.__dict__.copy()
