from . import utils


def load_objs(info):
    """
    Load the experiments/expname file for experiment-specific includes

    Parameters
    ----------
    info: list of str
        Experiment names to include
    """
    objs = {}
    modules = utils.interpret_list(info)
    experiments = ['experiments.' + m for m in modules]
    for experiment in experiments:
        module_objs = utils.extract_objs(experiment)
        objs.update(module_objs)
    return objs
