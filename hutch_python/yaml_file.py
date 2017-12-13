from . import utils


def load_objs(info):
    """
    Load arbitrary files for generic hutch-specific includes.

    Parameters
    ----------
    info: list
        Filenames or module names to include from current directory
    """
    objs = {}
    files = utils.interpret_list(info)
    for filename in files:
        module_objs = utils.extract_objs(filename)
        objs.update(module_objs)
    return objs
