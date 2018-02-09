import logging
from pathlib import Path
from subprocess import check_output, CalledProcessError, STDOUT

logger = logging.getLogger(__name__)
tstpython = Path(__file__).parent / 'tstpython'


def test_tstpython_scripts():
    logger.debug('test_tstpython_scripts')

    good_text = check_output([tstpython, 'script.py'])
    assert b'script ran' in good_text

    try:
        bad_text = check_output([tstpython, 'bad_script.py'], stderr=STDOUT)
    except CalledProcessError as err:
        bad_text = err.output
    assert b'Traceback' in bad_text
    assert b'ZeroDivisionError' in bad_text


def test_tstpython_ipython():
    logger.debug('test_tstpython_ipython')

    # This should show the banner and then exit, since we called it here when
    # we really can't call it here
    ipy_text = check_output([tstpython])
    assert b'IPython' in ipy_text
