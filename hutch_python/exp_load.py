import logging
from importlib import import_module
from types import SimpleNamespace

from .utils import safe_load

logger = logging.getLogger(__name__)


def get_exp_objs(proposal, run):
    """
    Load the correct experiment module.

    This will import User from ``experiments.{propsal}{run}``
    and create ``User()``, storing it as ``x``.

    Parameters
    ----------
    proposal: ``str``
        The proposal name, e.g. ``lp56``. This will be forced to
        lowercase for the import.

    run: ``str`` or ``int``
        The run number, e.g. 16

    Returns
    -------
    user: ``object`` or ``SimpleNamespace``
        Either the user's class instantiated or a blank namespace for other
        experiment-specific objects to be attached to.
    """
    logger.debug('get_exp_objs(%s, %s)', proposal, run)
    expname = proposal.lower() + str(run)
    module_name = 'experiments.' + expname
    with safe_load(expname):
        try:
            module = import_module(module_name)
            return module.User()
        except ImportError as exc:
            if module_name in exc.msg:
                logger.info('Skip missing experiment file %s.py', expname)
            else:
                raise
    return SimpleNamespace()
