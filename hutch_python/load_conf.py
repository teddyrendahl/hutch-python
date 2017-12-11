import yaml
import importlib
import logging

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
        All objects defined by the file, separated by original yml header.
    """
    with open(filename, 'r') as f:
        conf = yaml.load(f)
    all_objs = {}
    for header, info in conf.items():
        objs = []
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
    assembler = all_objs.get('namespace', None)
    if assembler is None:
        namespaces = {}
    else:
        namespaces = assembler(all_objs)
    all_objs.update(namespaces)
    return all_objs
