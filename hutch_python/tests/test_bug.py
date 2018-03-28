import os
import logging
import pathlib
import tempfile
import simplejson
from requests import Response

import hutch_python.bug
from hutch_python.bug import (get_current_environment, post_to_github,
                              report_bug)

logger = logging.getLogger(__name__)


# Mock user input function that just returns the prompt
def user_input(prompt):
    return prompt


# Mock requests.Session to avoid actual GitHub posts
class FakeSession:

    def __init__(self):
        self.auth = None

    def post(self, url, json_dump):
        r = Response()
        r.status_code = 201
        return r


def test_get_current_environment():
    logger.debug('test_get_current_environment')
    # Development packages
    fk_pkgs = ['one', 'two', 'three']
    os.environ['CONDA_ENVNAME'] = 'test-environment'
    with tempfile.TemporaryDirectory() as tmp:
        logger.debug('Creating temp directory {}', tmp)
        # Set a PythonPath
        os.environ['PYTHONPATH'] = tmp
        # Create fake packages
        for pkg in fk_pkgs:
            pathlib.Path(os.path.join(tmp, pkg)).touch()
        env, pkgs = get_current_environment()
        assert all([pkg in pkgs for pkg in fk_pkgs])
        assert env == 'test-environment'


def test_bug_report(monkeypatch):
    logger.debug('test_bug_report')
    # Patch in our fake user input function
    monkeypatch.setattr(hutch_python.bug, 'request_input', user_input)
    # Set a fake environment name
    os.environ['CONDA_ENVNAME'] = 'test-environment'
    with tempfile.TemporaryDirectory() as tmp:
        # Make sure we write to this directory
        hutch_python.bug.BUG_REPORT_PATH = tmp
        # Gather report
        bug_path = report_bug(captured_output='A printed message',
                              description='A description of the bug')
        bug = simplejson.load(open(bug_path, 'r'))
    # See that we catch the fake environment
    assert bug['env'] == 'test-environment'
    # See that bug reporting captures all keys
    bug_keys = ['author', 'commands', 'description', 'env', 'logfiles',
                'title', 'output', 'dev_pkgs']
    assert all([key in bug for key in bug_keys])


def test_post_to_github(monkeypatch):
    logger.debug('test_post_to_github')
    # Create a fake issue and requests.Session
    monkeypatch.setattr(hutch_python.bug.requests, 'Session', FakeSession)
    fake_post = {'title': 'This is a Test Issue'}
    with tempfile.NamedTemporaryFile('w+', delete=False) as tmp:
        simplejson.dump(fake_post, open(tmp.name, 'w+'))
        post_to_github(tmp.name, 'user', pw='pw')
        fname = tmp.name
    assert not os.path.exists(fname)
