Plugin Spec
===========
A ``Plugin`` class tells the loader how to interpret a segment of the yaml file.
All plugins will be stored in the ``hutch_python.plugins`` directory in a file
with the name ``pluginname.py`` containing a ``Plugin`` class that inherits from
``hutch_python.base_plugin.BasePlugin``. The specificatin for ``BasePlugin`` is
included below.

.. autoclass:: hutch_python.base_plugin.BasePlugin
   :members:
