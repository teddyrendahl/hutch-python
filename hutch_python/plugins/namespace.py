from types import SimpleNamespace
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
        objs = {}
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
            namespace = SimpleNamespace()
            for name in space_names:
                objs[name] = namespace
            logger.debug('Added class namespace for type %s as names %s',
                         cls, space_names)
            manager = ClassNamespaceManager(namespace, cls)
            managers.append(manager)
        return objs, managers


class NamespaceManager:
    def __init__(self, namespace):
        self.namespace = namespace

    def should_include(self, name, obj):
        return False

    def add(self, name, obj):
        if self.should_include(name, obj):
            setattr(self.namespace, name, obj)


class ClassNamespaceManager(NamespaceManager):
    def __init__(self, namespace, cls):
        super().__init__(namespace)
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
