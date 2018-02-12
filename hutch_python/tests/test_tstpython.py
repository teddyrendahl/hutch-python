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

    # This should show the banner, check if the name unique_device exists, and
    # then exit. There should be no NameError.
    ipy_text = check_output([tstpython], universal_newlines=True,
                            input='unique_device\n')
    assert 'IPython' in ipy_text
    assert 'NameError' not in ipy_text
