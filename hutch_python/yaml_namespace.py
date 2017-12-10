from types import SimpleNamespace
import logging

import utils

logger = logging.getLogger(__name__)


def load_objs(info):
    """
    Create a NameSpaceAssembler object based on the info from the
    yaml file. This will be used in the post-initialization step to organize
    objects into namespaces.
    """
    return NameSpaceAssembler(info)


class NameSpaceAssembler:
    def __init__(self, info):
        self.info = info

    def __call__(self, objs):
        all_spaces = {}
        for space, opts in self.info.items():
            spaces = {}
            if space in objs:
                spaces = self.source_space(objs[space], opts)
            else:
                assemble = getattr(self, space + "_space", None)
                if assemble is None:
                    logger.error('No handler for namespace %s', space)
                    continue
                spaces = assemble(objs, opts)
            all_spaces.update(spaces)

    def source_space(objs, opts):
        namespaces = {}
        namespace_names = utils.interpret_list(opts)
        named_obj = utils.assign_names(objs)
        for space_name in namespace_names:
            namespaces[space_name] = SimpleNamespace(**named_obj)
        return namespaces

    def class_space(objs, opts):
        pass
