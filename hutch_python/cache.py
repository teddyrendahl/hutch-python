from .utils import IterableNamespace
import sys


class LoadCache:
    """
    Create a virtual module to store objects. This virtual module can be
    imported from as if it were a normal module.

    Attributes
    ----------
    objs: IterableNamespace
        This is a namespace containing all the objects that have been attached
        to the LoadCache.
    """
    def __init__(self, module, **objs):
        """
        Parameters
        ----------
        module: str
            Name of the virtual module to create. If the module has the same
            name as a real module, the real module will be masked.

        **objs: kwargs
            Initial objects to place into the namespace
        """
        self.objs = IterableNamespace(**objs)
        sys.modules[module] = self.objs

    def __call__(self, **objs):
        """
        Add objects to the namespace.

        Parameters
        ----------
        **objs: kwargs
            The key will be the namespace-accessible name, and the object
            should be the object we are adding.
        """
        self.objs.__dict__.extend(**objs)
