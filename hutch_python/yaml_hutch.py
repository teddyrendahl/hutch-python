import utils


def load_objs(info):
    """
    Load the hutch.py file for generic hutch-specific includes.
    """
    objs = []
    files = utils.interpret_list(info)
    for filename in files:
        module_objs = utils.extract_objs(filename)
        objs.extend(module_objs)
    return objs
