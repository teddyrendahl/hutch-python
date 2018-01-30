from types import SimpleNamespace
from collections import defaultdict
import inspect
import logging

from ..base_plugin import BasePlugin
from .. import utils

logger = logging.getLogger(__name__)


class Plugin(BasePlugin):
    """
    Plugin to organize the user namespaces
    """
    priority = 10
    name = 'namespace'

    def get_objects(self):
        return_objs = {}
        self.namespace_managers = []
        for space, opts in self.info.items():
            logger.debug('Loading %s namespaces', space)
            if space == 'class':
                objs, managers = self.get_class_objects(opts)
            elif space == 'metadata':
                objs, managers = self.get_metadata_objects(opt)
            else:
                err = 'Namespace {} not defined'
                logger.warning(err.format(space))
                continue
            return_objs.update(objs)
            self.namespace_managers.extend(managers)
        return return_objs

    def future_object_hook(self, name, obj):
        for manager in self.namespace_managers:
            manager.add(name, obj)

    def get_class_objects(self, opts):
        objs = defaultdict(SimpleNamespace)
        managers = []
        for cls_name, space_names in opts.items():
            try:
                if cls_name == 'function':
                    cls = 'function'
                else:
                    cls = utils.find_class(cls_name)
            except Exception as exc:
                cls = None
                err = 'Type {} could not be loaded'
                logger.error(err.format(cls_name))
                logger.debug(exc, exc_info=True)
                continue
            for name in space_names:
                namespace = objs[name]
                manager = ClassNamespaceManager(namespace, name, cls)
                managers.append(manager)
                logger.debug('Added class namespace for type %s as name %s',
                             cls, name)
        return objs, managers

    def get_metadata_objects(self, opts):
        objs = {'md': SimpleNamespace()}
        managers = [MetadataNamespaceManager(objs['md'], 'md', opts)]
        return objs, managers


class NamespaceManager:
    def __init__(self, namespace, name):
        self.namespace = namespace
        self.name = name

    def should_include(self, name, obj):
        raise NotImplementedError('Need to subclass should_include')

    def add(self, name, obj):
        if self.should_include(name, obj):
            logger.debug('Add %s to namespace %s', name, self.name)
            setattr(self.namespace, name, obj)


class ClassNamespaceManager(NamespaceManager):
    def __init__(self, namespace, name, cls):
        super().__init__(namespace, name)
        self.cls = cls

    def should_include(self, name, obj):
        if self.cls == 'function':
            if inspect.isfunction(obj):
                return True
            else:
                return False
        elif isinstance(obj, self.cls):
            return True
        else:
            return False


class MetadataNamespaceManager(NamespaceManager):
    def __init__(self, namespace, name, filters):
        super().__init__(namespace, name)
        self.filters = filters

    def should_include(self, name, obj):
        return hasattr(obj, 'md')

    def add(self, name, obj):
        if self.should_include(name, obj):
            logger.debug('Add %s to namespace %s', name, self.name)
            upper_space = self.namespace
            for filt in self.filters:
                key = getattr(obj.md, filt, None)
                if key is None:
                    setattr(upper_space, name, obj)
                    return
                key = key.lower()
                if name.startswith(key):
                    name = name[len(key)+1:]
                if not hasattr(upper_space, key):
                    setattr(upper_space, key, SimpleNamespace())
                upper_space = getattr(upper_space, key)
            setattr(upper_space, name, obj)
