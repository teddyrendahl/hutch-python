from types import SimpleNamespace
from collections import defaultdict
import inspect
import logging

from ..base_plugin import BasePlugin
from .. import utils
import hutch_python

logger = logging.getLogger(__name__)


class Plugin(BasePlugin):
    """
    Plugin to organize the user namespaces
    """
    priority = -10
    name = 'namespace'

    def get_objects(self):
        prev_objs = {}
        for plugin_name in hutch_python.plugin_loads:
            namespace = getattr(hutch_python, plugin_name)
            prev_objs.update(namespace.__dict__)

        return_objs = {}
        for space, opts in self.info.items():
            logger.debug('Loading %s namespaces', space)
            if space == 'class':
                new_objs = self.get_class_objs(opts, prev_objs)
            elif space == 'metadata':
                new_objs = self.get_metadata_objs(opts, prev_objs)
            else:
                err = 'Namespace {} not defined'
                logger.warning(err.format(space))
                continue
            return_objs.update(new_objs)
        return return_objs

    def get_class_objs(self, opts, prev_objs):
        class_objs = defaultdict(SimpleNamespace)
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

    def get_metadata_objs(self, opts, prev_objs):
        metadata_objs = defaultdict(SimpleNamespace)
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
                        setattr(upper_space, key, SimpleNamespace())
                    upper_space = getattr(upper_space, key)
                setattr(upper_space, name, obj)
        return metadata_objs

    def strip_prefix(self, name, strip_text):
        if name.startswith(strip_text):
            return name[len(strip_text)+1:]
        else:
            return name
