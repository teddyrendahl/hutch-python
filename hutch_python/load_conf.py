import logging
import yaml
import datetime
from importlib import import_module
from collections import defaultdict
from pathlib import Path

import pyfiglet

import hutch_python

HUTCH_COLORS = dict(
    amo='38;5;27',
    sxr='38;5;250',
    xpp='38;5;40',
    xcs='38;5;93',
    mfx='38;5;202',
    cxi='38;5;96',
    mec='38;5;214')
logger = logging.getLogger(__name__)


def load(filename):
    """
    Load the hutch-specific conf.yml file.

    Parameters
    ----------
    filename: str
        Path to the conf.yml file

    Returns
    -------
    objs: dict{str: object}
        All objects defined by the file that need to make it into the
        environment. The strings are the names that will be accessible in the
        global namespace.
    """
    with open(filename, 'r') as f:
        conf = yaml.load(f)
    hutch_banner(conf.get('hutch', 'hutch').lower())
    return read_conf(conf, filename)


def read_conf(conf, filename=None):
    """
    Parameters
    ----------
    conf: dict
        dict interpretation of the original yaml file

    filename: str, optional
        Path to the conf.yml file. If provided, we can include all the created
        objects in a special hutch.db module.

    Returns
    ------
    objs: dict{str: object}
        Return value of load
    """
    hutch_python.clear_load()
    plugins = get_plugins(conf)
    hutch = conf.get('hutch')
    if filename is None:
        objects = run_plugins(plugins)
    elif hutch is not None:
        conf_path = Path(filename)
        hutch_path = conf_path.parent
        objects = run_plugins(plugins, hutch=hutch, hutch_path=hutch_path)
    return objects


def get_plugins(conf):
    """
    Parameters
    ----------
    conf: dict
        dict interpretation of the original yaml file

    Returns
    -------
    plugins: dict{int: list}
        Mapping from priority level to list of instantiated plugins at that
        prority.
    """
    plugins = defaultdict(list)

    for plugin_name, info in conf.items():
        try:
            module = import_module('hutch_python.plugins.' + plugin_name)
        except ImportError:
            module = None
            err = 'Plugin {} is not available, skipping'
            logger.warning(err.format(plugin_name))
            continue
        this_plugin = module.Plugin(conf, info)
        try:
            pre_plugins = this_plugin.pre_plugins()
        except Exception:
            pre_plugins = []
            err = 'Error in {} pre-plugins, skipping'
            logger.warning(err.format(plugin_name))
        for plugin in pre_plugins + [this_plugin]:
            plugins[this_plugin.priority].append(plugin)

    return plugins


def run_plugins(plugins, hutch=None, hutch_path=None):
    """
    Create all of the objects, given plugin instructions.

    Parameters
    ----------
    plugins: dict{int: list}
        Return value from get_plugins

    hutch: str, optional
        Hutch to create the objects for. If included and conf_dir is also
        included, we'll put objects into the hutch.db module as we go.

    hutch_path: Path, optional
        Path to the hutch's directory with the configuration file. This is
        expected to at least have a hutchname directory with an __init__.py
        file inside it.

    Returns
    ------
    objs: dict{str: object}
        Return value of load
    """
    all_objs = {}

    # Dummy module for easier user imports
    do_db = None not in (hutch, hutch_path)
    if do_db:
        db_module_name = hutch + '.db'
        db_path = hutch_path / hutch / 'db.py'
        if not db_path.exists():
            db_path.touch()
        db_module = import_module(db_module_name)

    plugin_priorities = reversed(sorted(list(plugins.keys())))
    executed_plugins = []

    for prio in plugin_priorities:
        for this_plugin in plugins[prio]:
            try:
                objs = this_plugin.get_objects()
            except Exception as exc:
                objs = None
                err = 'Plugin {} failed to load, skipping'
                logger.error(err.format(this_plugin.name))
                logger.debug(exc, exc_info=True)
                continue
            for past_plugin in executed_plugins:
                try:
                    past_plugin.future_plugin_hook(this_plugin.name, objs)
                except Exception as exc:
                    err = 'Plugin {} post-hook failed for plugin {}'
                    logger.error(err.format(past_plugin.name,
                                            this_plugin.name))
                    logger.debug(exc, exc_info=True)
            executed_plugins.append(this_plugin)
            all_objs.update(objs)
            # Update db file as we go
            if do_db:
                for name, obj in objs.items():
                    setattr(db_module, name, obj)
            hutch_python.register_load(this_plugin.name, objs)

    # Annotate db file at the end
    if do_db:
        quotes = '"""\n'
        header = 'Automatically generated file, do not edit.\n\n'
        body = ('hutch-python last loaded on {}\n'
                'with the following objects:\n\n')
        text = quotes + header + body.format(datetime.datetime.now())
        for name, obj in all_objs.items():
            text += '{:<20} {}\n'.format(name, obj.__class__)
        text += quotes
        with db_path.open('w') as f:
            f.write(text)

    return all_objs


def hutch_banner(hutch_name):
    text = hutch_name + 'Python'
    f = pyfiglet.Figlet(font='big')
    banner = f.renderText(text)
    if hutch_name in HUTCH_COLORS:
        banner = '\x1b[{}m'.format(HUTCH_COLORS[hutch_name]) + banner
    print(banner)
