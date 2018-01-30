import logging
from unittest.mock import patch

import pytest

import hutch_python.plugins.questionnaire
from hutch_python.plugins.questionnaire import Plugin


logger = logging.getLogger(__name__)


@pytest.fixture(scope='module')
def patch_questionnaire():
    class QSBackend:
        def __init__(self, run, proposal):
            self.run = run
            self.proposal = proposal

        def find(self, multiples=False, **kwargs):
            devices = [{
                '_id': 'TST:USR:MMN:01',
                'beamline': 'TST',
                'device_class': 'hutch_python.tests.conftest.Experiment',
                'location': 'Hutch-main experimental',
                'args': ['{{run}}', '{{proposal}}'],
                'kwargs': {},
                'name': 'inj_x',
                'prefix': 'TST:USR:MMN:01',
                'purpose': 'Injector X',
                'type': 'Device',
                'run': self.run,
                'proposal': self.proposal}]
            if multiples:
                return devices
            else:
                return devices[0]

    with patch('hutch_python.plugins.questionnaire.QSBackend') as qs_db:
        qs_db.return_value = QSBackend
        yield QSBackend


def test_questionnaire_plugin(patch_questionnaire):
    logger.debug("test_questionnaire_plugin")
    conf = {'experiment': {'run': '15', 'proposal': 'LR12'},
            'questionnaire': True}
    plugin = Plugin(conf)
    hutch_python.plugins.questionnaire.QSBackend = patch_questionnaire
    objs = plugin.get_objects()
    assert objs['inj_x'].run == '15'
    assert objs['inj_x'].proposal == 'LR12'
