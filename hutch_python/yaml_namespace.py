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
    """
    Used in post-initialization to organize objects into namespaces.
    """
    def __init__(self, info):
        """
        Parameters
        ----------
        info: dict
            Mapping from namespace catagory to options. This should come from
            loading a yaml file, and should be the sub-dictionary under the
            top-level namespace key.
        """
        self.info = info

    def __call__(self, objs):
        return self.assemble(objs)

    def assemble(self, objs):
        """
        Parameters
        ----------
        objs: dict
            Mapping from top-level yaml header to either lists of objects or
            dictionaries that map name to object. This should exhaustively
            include all the objects that we've loaded.

        Returns
        -------
        namespaces: dict
            Mapping from namespace name to namespace
        """
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
        """
        Group objects into namespaces by source. This is the trivial one since
        we group them by source as we create them. To reach this block, we need
        a subheader under namespace that matches a previous top-level header.

        Parameters
        ----------
        objs: list
            List of objects under the chosen header

        opts: list
            List of names to alias this namespace

        Returns
        -------
        namespaces: dict
            Mapping from namespace name to namespace
        """
        namespaces = {}
        namespace_names = utils.interpret_list(opts)
        named_obj = utils.assign_names(objs)
        for space_name in namespace_names:
            namespaces[space_name] = SimpleNamespace(**named_obj)
        return namespaces

    def class_space(objs, opts):
        """
        Group objects into namespaces by Python type. Subclasses are included.

        Parameters
        ----------
        objs: dict
            Mapping from source header to list of objects or dict of name to
            object.

        opts: dict
            Mapping from type to namespace aliases. Types must be represented
            as strings, so they either must be built-ins or importable from the
            string path.

        Returns
        -------
        namespaces: dict
            Mapping from namespace name to namespace
        """
        namespaces = {}
        for class_path, name in opts.items():
            space_info = {}
            for object_group in objs.values():
                if isinstance(object_group, list):
                    space_info.update(utils.assign_names(object_group))
                elif isinstance(object_group, dict):
                    space_info.update(object_group)
                else:
                    raise TypeError('Invalid type %s in arg to class_space',
                                    type(objs))
            namespaces[name] = SimpleNamespace(**space_info)
        return namespaces
