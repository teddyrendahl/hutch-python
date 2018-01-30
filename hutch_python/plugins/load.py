import logging
from importlib import import_module
from types import SimpleNamespace

from ..base_plugin import BasePlugin
from .. import utils

logger = logging.getLogger(__name__)


class Plugin(BasePlugin):
    """
    Plugin to load arbitrary files for generic hutch-specific includes.
    """
    name = 'load'

    def get_objects(self):
        objs = {}
        # Determine instructions from `import`
        all_instructions = self.info['import'].split(' as ')
        import_instructions = all_instructions[0]
        try:
            naming_instructions = all_instructions[1]
        except IndexError:
            naming_instructions = None
        # Import objects as instructed by config
        objs = self.do_import(import_instructions)
        objs = self.do_naming(naming_instructions, objs)
        return objs

    def do_import(self, import_instructions):
        """
        Parse lines like:
            'experiment'        -> get all the objects
            'experiment.user'   -> get the object named user
            'experiment.User()' -> get the class named User and make an object
        """
        logger.debug('Using import instructions "%s"', import_instructions)
        # Attempt straight import
        objs = utils.extract_objs(import_instructions)
        if '.' in import_instructions:
            module_name, name = import_instructions.rsplit('.', 1)
            try:
                obj = import_module(name, package=module_name)
            except ModuleNotFoundError as exc:
                logger.debug("Import instructions is not a module, but an "
                             "object")
                # If the import has parantheses we know that it is an object of
                # some sort
                is_class = False
                if '()' in name:
                    is_class = True
                    name = name.strip('()')
                module = import_module(module_name)
                obj = getattr(module, name)
                if is_class:
                    obj = obj()
            # Store the object with the proper name
            objs = {name.lower(): obj}
        else:
            # If there is no . assume that either the import instructions is a
            # valid Python module
            objs = utils.extract_objs(import_instructions)
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
