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
    objs: list
        All objects defined by the file
    """
    with open(filename, 'r') as f:
        conf = yaml.load(f)[0]
    all_objs = []
    for module, info in conf.items():
        objs = []
        try:
            loader = importlib.import_module('hutch_python.yaml_' + module)
        except ImportError:
            err = 'ImportError when including %s. Skipping.'
            logger.exception(err, module)
            continue
        try:
            objs = loader.load_objs(info)
        except Exception:
            err = 'Exception thrown when building %s objects. Skipping'
            logger.exception(err, module)
            continue
        all_objs.extend(objs)
