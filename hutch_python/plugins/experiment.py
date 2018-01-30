import logging
from importlib import import_module
from types import SimpleNamespace

from ..base_plugin import BasePlugin
from .. import utils

logger = logging.getLogger(__name__)


class Plugin(BasePlugin):
    """
    Plugin to load experiment-spefic includes.

    By default, the Experiment plugin attempts to load information from the
    PCDS Questionnaire. You can disable this by setting, ``questionnaire:
    False`` underneath the ``experiment`` section in your YAML configuration
    """
    name = 'experiment'

    def pre_plugins(self):
        if self.info.get('questionnaire', True):
            from .questionnaire import Plugin as QSPlugin
            return [QSPlugin(conf=self.conf)]

    def get_objects(self):
        expname = self.info['name']
        if expname[:4] == 'auto':
            expname = self.get_experiment_name()
        logger.info('Loading experiment %s', expname)

        module_name = 'experiments.' + expname
        all_instructions = self.info['import'].split(' as ')
        import_instructions = all_instructions[0]
        try:
            naming_instructions = all_instructions[1]
        except IndexError:
            naming_instructions = None

        objs = self.do_import(import_instructions, module_name)
        objs = self.do_naming(naming_instructions, objs)
        return objs

    def do_import(self, import_instructions, module_name):
        """
        Parse lines like:
            'experiment'        -> get all the objects
            'experiment.user'   -> get the object named user
            'experiment.User()' -> get the class named User and make an object
        """
        logger.debug('Using import instructions "%s"', import_instructions)
        if '.' in import_instructions:
            module = import_module(module_name)
            name = import_instructions.split('.')[1]

            is_class = False
            if '()' in name:
                is_class = True
                name = name.strip('()')

            obj = getattr(module, name)
            if is_class:
                obj = obj()

            objs = {name.lower(): obj}
        else:
            objs = utils.extract_objs(module_name)
        return objs

    def do_naming(self, naming_instructions, objs):
        """
        Parse the back half of lines like:
            'experiment'                   -> do nothing
            'experiment as x'              -> all objs as namespace x
            'experiment.User() as x, exp'  -> one obj as x and as exp
        """
        logger.debug('Using naming instructions "%s"', naming_instructions)
        if naming_instructions is None:
            return objs
        else:
            return_objs = {}
            names = naming_instructions.split(',')
            for name in names:
                name = name.strip(' ')
                name = name.replace(' ', '_')
                if len(objs) == 1:
                    return_objs[name] = list(objs.values())[0]
                else:
                    return_objs[name] = SimpleNamespace(**objs)
            return return_objs

    def get_experiment_name(self):
        raise NotImplementedError('No hook into pswww for exp name yet')
