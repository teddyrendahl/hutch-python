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


def load(cfg=None, db=None):
    """
    Read the config file and the database entries.
    From this information we can:
        - Display the banner by calling `hutch_banner`
        - Find the hutch's launch directory
        - Load the hutch's objects by calling `read_conf`

    Parameters
    ----------
    cfg: str, optional
        Path to the conf.yml file. If this is missing, we'll end up with a very
        empty environment.

    Returns
    -------
    objs: dict{str: object}
        All objects defined by the files that need to make it into the
        environment. The strings are the names that will be accessible in the
        global namespace.
    """
    if cfg is None:
        hutch_banner('hutch')
        return read_conf({})
    else:
        with open(cfg, 'r') as f:
            conf = yaml.load(f)
        hutch_banner(conf.get('hutch', 'hutch').lower())
        conf_path = Path(cfg)
        hutch_dir = conf_path.parent
        return load_conf(conf, hutch_dir=hutch_dir)


def load_conf(conf, hutch_dir=None):
    """
    Step through the objcet loading procedure, consulting conf as needed.
    The procedure is:
        - Use 'hutch' conf to create hutch.db importable namespace to stash the
          objects. This will be literally hutch.db if hutch is not provided, or
          the hutch name e.g. mfx.db
        - Create a `RunEngine`
        - import and group basic plans into an importable namespace
        - Use 'hutch' conf to create a Daq object and add daq plan tools into
          the plans namespace
        - Use 'db' conf to load devices from happi beamline database
        - Use 'load' conf to bring up the user's beamline files
        - Use 'experiment' conf to select the current experiment
            - If 'experiment' was missing, autoselect experiment using 'hutch'
        - Use current experiment to load experiment objects from questionnaire
        - Use current experiment to load experiment file

    If a conf entry is missing, we'll note it in a logger.info message.
    If an extra conf entry is found, we'll note it in a logger.warning message.
    If an automatically selected file is missing, we'll note it in a
    logger.warning message.
    All other errors will be noted in a logger.error message.

    Parameters
    ----------
    conf: dict
        dict interpretation of the original yaml file

    hutch_dir: Path or str, optional
        Path object that points to the hutch's launch directory. This is the
        directory that includes the 'experiments' directory and a hutchname
        directory e.g. mfx
        If this is missing we'll be starting a mostly empty session.

    db: Path or str, optional
        Path object that points to a happi database. This currently only
        support the json file format.

    Returns
    ------
    objs: dict{str: object}
        Return value of load
    """
    # Warn user about excess config entries
    valid_keys = ('hutch', 'db', 'load', 'experiment')
    for key in conf:
        if key not in valid_keys:
            txt = ('Found %s in configuration, but this is not a valid key. '
                   'The valid keys are %s')
            logger.warning(txt, key, valid_keys)

    # Grab configurations from dict, set defaults, show missing
    try:
        hutch = conf['hutch']
    except KeyError:
        hutch = None
        logger.info('Missing hutch from conf. Will skip DAQ.')
    try:
        db = Path(conf['db'])
    except KeyError:
        db = None
        logger.info(('Missing db from conf. Will skip loading from shared '
                     'database.'))
    try:
        load = conf['load']
    except KeyError:
        load = None
        logger.info('Missing load from conf. Will skip loading hutch files.')

    try:
        experiment = conf['experiment']
    except KeyError:
        experiment = None
        if hutch is None:
            logger.info(('Missing hutch and experiment from conf. Will not '
                         'load objects from questionnaire or experiment '
                         'file.'))

    # Make cache namespace
    cache = LoadCache(module=hutch or 'hutch', cache_name='db')

    # Make RunEngine
    RE = RunEngine({})
    cache(RE=RE)

    # Collect Plans
    plans = import_module('.plan_defaults')
    cache(plans=plans)
    cache(p=plans)

    # Daq
    if hutch is not None:
        daq_objs = get_daq_objs(hutch, RE)
        cache(**daq_objs)

    # Happi db
    if db is not None:
        happi_objs = get_happi_objs(db)
        cache(**happi_objs)

    # Load user files
    if load is not None:
        load_objs = get_load_objs(load)
        cache(**load_objs)

    # Auto select experiment if we need to
    if experiment is None:
        if hutch is not None:
            try:
                experiment = get_current_experiment(hutch)
                logger.info('Selected experiment %s', experiment)
            except Exception:
                err = 'Failed to select experiment automatically'
                logger.error(err)
                logger.debug(err, exc_info=True)

    # Experiment objects
    if experiment is not None:
        qs_objs = get_qs_objs(experiment)
        cache(**qs_objs)
        exp_objs = get_exp_objs(experiment)
        cache(**exp_objs)

    return cache.objs



#    all_objs = {}
#
#    # Dummy module for easier user imports
#    do_db = None not in (hutch, hutch_path)
#    if do_db:
#        db_module_name = hutch + '.db'
#        db_path = hutch_path / hutch / 'db.py'
#        if not db_path.exists():
#            db_path.touch()
#        db_module = import_module(db_module_name)
#
#    # Annotate db file at the end
#    if do_db:
#        quotes = '"""\n'
#        header = ('The objects referenced in this file are populated by the '
#                  '{0}python\ninitialization. If you wish to use devices '
#                  'from this file, import\nthem from {0}.db after calling the '
#                  '{0}python startup script.\n\n'.format(hutch))
#        body = ('hutch-python last loaded on {}\n'
#                'with the following objects:\n\n')
#        text = quotes + header + body.format(datetime.datetime.now())
#        for name, obj in all_objs.items():
#            text += '{:<20} {}\n'.format(name, obj.__class__)
#        text += quotes
#        with db_path.open('w') as f:
#            f.write(text)
#
#    return all_objs


def hutch_banner(hutch_name):
    text = hutch_name + 'Python'
    f = pyfiglet.Figlet(font='big')
    banner = f.renderText(text)
    if hutch_name in HUTCH_COLORS:
        banner = '\x1b[{}m'.format(HUTCH_COLORS[hutch_name]) + banner
    print(banner)
