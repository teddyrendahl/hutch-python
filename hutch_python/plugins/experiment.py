import logging

from ..base_plugin import BasePlugin
from .. import utils
from .load import Plugin as FilePlugin

logger = logging.getLogger(__name__)


class Plugin(BasePlugin):
    """
    Plugin to load experiment-spefic includes.
    """
    name = 'experiment'

    def pre_plugins(self):
        plugins = list()
        # As long as questionnaire isn't specifically set to False
        # attempt to load information via the QuestionnairePlugin
        if self.info.get('questionnaire', True):
            from .questionnaire import Plugin as QSPlugin
            plugins.append(QSPlugin(conf=self.conf))
        # Also load the specific experiment file
        expname = self.info['name']
        # If there are no specific import instructions assume the most basic
        # import of a file import with no renaming
        import_instruct = self.info.get('import', 'experiment')
        # Determine the proper module name of the experiment file and
        # substitute
        if expname[:4] == 'auto':
            expname = self.get_experiment_name()
        logger.info('Loading experiment %s', expname)
        module_name = 'experiments.' + expname
        import_instruct = import_instruct.replace('experiment', module_name)
        plugins.append(FilePlugin(info={'import': import_instruct}))
        return plugins

    def get_objects(self):
        return dict()

    def get_experiment_name(self):
        raise NotImplementedError('No hook into pswww for exp name yet')
