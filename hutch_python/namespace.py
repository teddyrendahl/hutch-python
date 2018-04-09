"""
This module provides utilities for grouping objects into namespaces.
"""
from inspect import isfunction
import logging

from ophyd import Device

from .utils import (IterableNamespace, find_class, strip_prefix,
                    extract_objs)

logger = logging.getLogger(__name__)


def class_namespace(cls, scope=None):
    """
    Create a ``namespace`` that contains objects of a specific type.

    Parameters
    ----------
    cls: ``type`` or ``str``

    scope: ``module``, ``namespace``, or ``list`` of these
        Every object attached to the given modules will be considered for the
        `class_namespace`. If ``scope`` is omitted, we'll check all objects
        loaded by ``hutch-python`` and everything in the caller's global frame.
        If anything is an instance of ``ophyd.Device``, we'll also include the
        object's components as part of the scope, using the ``name`` attribute
        to identify them rather than the attribute name on the device. This
        will continue recursively.

    Returns
    -------
    namespace: `IterableNamespace`
    """
    logger.debug('Create class_namespace cls=%s, scope=%s', cls, scope)
    class_space = IterableNamespace()
    scope_objs = extract_objs(scope=scope, stack_offset=1)

    if isinstance(cls, str):
        if cls != 'function':
            try:
                cls = find_class(cls)
            except Exception as exc:
                err = 'Type {} could not be loaded'
                logger.error(err.format(cls))
                logger.debug(exc, exc_info=True)
                return class_space

    # Mapping from Device class to subdevices of the correct type
    cache = {}

    def isinstance_ext(obj, desired_cls):
        """
        isinstance extended for functions because Python is dumb
        """
        include = False
        if cls == 'function':
            if isfunction(obj):
                include = True
        elif isinstance(obj, cls):
            include = True
        return include

    def inspect_device_cls(device_cls, desired_cls, attr_path=None):
        """
        Get a list of components of device_class that match desired_cls,
        skipping lazy components.
        """
        attrs = []
        if issubclass(device_cls, Device):
            logger.debug('Checking subdevices for class %s', device_cls)
            for cpt_name in device_cls.component_names:
                cpt = getattr(device_cls, cpt_name)
                if not cpt.lazy:
                    if attr_path is None:
                        sub_attr_path = [cpt_name]
                    else:
                        sub_attr_path = attr_path + [cpt_name]
                    if issubclass(cpt.cls, desired_cls):
                        attrs.append(sub_attr_path)
                    subattrs = inspect_device_cls(cpt.cls, desired_cls,
                                                  sub_attr_path)
                    attrs.extend(subattrs)
            logger.debug('Class %s has matching subdevices %s',
                         device_cls, attrs)
        return attrs

    def add_to_space(obj, obj_name, desired_cls, cache, namespace):
        """
        Helper function to add one object to the namespace, and possibly
        subdevices, or not.
        """
        if isinstance_ext(obj, desired_cls):
            logger.debug('Adding %s to %s namespace', obj_name, desired_cls)
            setattr(namespace, obj_name, obj)
        if isinstance(obj, Device):
            obj_cls = obj.__class__
            if obj_cls not in cache:
                cache[obj_cls] = inspect_device_cls(obj_cls, desired_cls)
            subdevice_attrs = cache[obj_cls]
            for attrs in subdevice_attrs:
                device = obj
                for attr in attrs:
                    device = getattr(device, attr)
                logger.debug('Adding %s to %s namespace',
                             device.name, desired_cls)
                setattr(namespace, device.name, device)

    for name, obj in scope_objs.items():
        add_to_space(obj, name, cls, cache, class_space)

    return class_space


def metadata_namespace(md, scope=None):
    """
    Create a ``namespace`` that accumulates objects and creates a tree based on
    their metadata.

    Parameters
    ----------
    md: ``list`` of ``str``
        Each of the metadata categories to group objects by, in order from the
        root of the tree to the leaves.

    scope: ``module``, ``namespace``, or ``list`` of these
        Every object attached to the given modules will be considered for the
        `metadata_namespace`. If ``scope`` is omitted, we'll check all objects
        loaded by ``hutch-python`` and everything in the caller's global frame.

    Returns
    -------
    namespace: `IterableNamespace`
    """
    logger.debug('Create metadata_namespace md=%s, scope=%s', md, scope)
    metadata_space = IterableNamespace()
    scope_objs = extract_objs(scope=scope, stack_offset=1)

    for name, obj in scope_objs.items():
        # Collect obj metadata
        if hasattr(obj, 'md'):
            raw_keys = [getattr(obj.md, filt, None) for filt in md]
        # Fallback: use_the_name
        else:
            if '_' not in name:
                continue
            name_keys = name.split('_')
            raw_keys = name_keys[:len(md)]
        # Abandon if no matches
        if raw_keys[0] is None:
            continue
        # Force lowercase
        keys = []
        for key in raw_keys:
            if isinstance(key, str):
                keys.append(key.lower())
            else:
                keys.append(key)
        # Add key to existing namespace branch, create new if needed
        logger.debug('Add %s to metadata namespace', name)
        upper_space = metadata_space
        for key in keys:
            if key is None:
                break
            name = strip_prefix(name, key)
            if not hasattr(upper_space, key):
                setattr(upper_space, key, IterableNamespace())
            upper_space = getattr(upper_space, key)
        setattr(upper_space, name, obj)
    return metadata_space
