from pathlib import Path

CUR_EXP_SCRIPT = '/reg/g/pcds/engineering_tools/{0}/scripts/get_curr_exp {0}'

CLASS_SEARCH_PATH = ['pcdsdevices.device_types']

DAQ_MAP = dict(amo=0,
               sxr=0,
               xpp=1,
               xcs=1,
               mfx=4,
               cxi=4,
               mec=0,
               tst=0)

DIR_MODULE = Path(__file__).resolve().parent

FILE_YAML = DIR_MODULE / 'logging.yml'

HUTCH_COLORS = dict(
    amo='38;5;27',
    sxr='38;5;250',
    xpp='38;5;40',
    xcs='38;5;93',
    mfx='38;5;202',
    cxi='38;5;96',
    mec='38;5;214')

INPUT_LEVEL = 5

SUCCESS_LEVEL = 35

VALID_KEYS = ('hutch', 'db', 'load', 'experiment')
