import yaml
import importlib
import logging

from . import utils

logger = logging.getLogger(__name__)


def load(filename):
    """
    Load the hutch-specific conf.yml file.

    Parameters
    ----------
    filename: str
        Path the conf.yml file

    Returns
    -------
    objs: dict{str: Object}
        All objects defined by the file that need to make it into the
        environment. The strings are the names that will be accessible in the
        global namespace.
    """
    with open(filename, 'r') as f:
        conf = yaml.load(f)
    all_objs = {}
    for header, info in conf.items():
        objs = {}
        try:
            loader = importlib.import_module('hutch_python.yaml_' + header)
        except ImportError:
            err = 'ImportError when including %s. Skipping.'
            logger.exception(err, header)
            continue
        try:
            objs = loader.load_objs(info)
        except Exception:
            err = 'Exception thrown when building %s objects. Skipping'
            logger.exception(err, header)
            continue
        all_objs[header] = objs
    return_dict = {}
    for object_grouping in all_objs.values():
        if isinstance(object_grouping, list):
            mapping = utils.assign_names(object_grouping)
            return_dict.update(mapping)
        elif isinstance(object_grouping, dict):
            return_dict.update(object_grouping)
    assembler = all_objs.get('namespace', None)
    if assembler is not None:
        namespaces = assembler(all_objs)
        return_dict.update(namespaces)
    return return_dict
