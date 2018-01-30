import logging

import pytest

import hutch_python.plugins.questionnaire
from hutch_python.plugins.questionnaire import Plugin

from ..conftest import QSBackend

logger = logging.getLogger(__name__)


def test_questionnaire_plugin():
    logger.debug("test_questionnaire_plugin")
    conf = {'experiment': {'run': '15', 'proposal': 'LR12'},
            'questionnaire': True}
    plugin = Plugin(conf)
    hutch_python.plugins.questionnaire.QSBackend = QSBackend
    objs = plugin.get_objects()
    assert objs['inj_x'].run == '15'
    assert objs['inj_x'].proposal == 'LR12'


def test_questionnaire_bad_conf():
    logger.debug('test_questionnaire_bad_conf')
    conf = {'experiment': {}, 'questionnaire': True}
    plugin = Plugin(conf)
    hutch_python.plugins.questionnaire.QSBackend = QSBackend
    with pytest.raises(ValueError):
        plugin.get_objects()
