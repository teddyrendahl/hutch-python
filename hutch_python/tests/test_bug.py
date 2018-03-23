import os
import logging
from unittest.mock import patch

import hutch_python.bug
from hutch_python.bug import report_bug

logger = logging.getLogger(__name__)


def user_input(prompt):
    return prompt

def test_bug_report(monkeypatch):
    logger.debug('test_bug_report')
    # Patch in our fake user input function
    monkeypatch.setattr(hutch_python.bug, 'request_input', user_input)
    # Set a fake environment name
    os.environ['CONDA_ENVNAME'] = 'test-environment'
    # Gather report
    bug = report_bug(captured_output='A printed message',
                     description='A description of the bug')
    # See that we catch the fake environment
    assert bug['env'] == 'test-environment'
    # See that bug reporting captures all keys
    bug_keys = ['author', 'commands', 'description', 'env', 'logfiles',
                'title', 'output', 'dev_pkgs']
    assert all([key in bug for key in bug_keys])
