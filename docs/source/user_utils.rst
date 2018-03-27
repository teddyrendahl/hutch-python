Useful Utilities
================

Reporting Issues
----------------
.. automodule:: hutch_python.bug

   .. autofunction:: report_bug

Issue Lifecyle
^^^^^^^^^^^^^^
We can not expect that every operator on the beamline has a valid Github
account. To get around this, when you call `report_bug` we dump a JSON
description of the issue into a standard NFS directory. Then by a regular CRON
job we will post this issue to https://github.com/pcdshub/Bug-Reports. This
leads to a slight delay but also allows to have issues posted by persons
without valid GitHub accounts. Once issues are received on GitHub the
appropriate action will be made by the PCDS staff. This may mean a deeper look
at the linked log files and/or creating a distilled issue or action item in a
different repository. 

Safe Loading
------------
`hutch_python.utils.safe_load` can be used as a shortcut for wrapping code
that may or may not succeed to prevent a bad submodule from interrupting the
``hutch-python`` load sequence. This means that if the ``Attenuator`` class is
bugging out, we'll be warned that there is a problem and skip it, but you'll
still be able to manipulate the ``Slits`` objects.

For example, this will complete successfully but show a warning:

.. ipython:: python

    from hutch_python.utils import safe_load

    with safe_load('divide by zero'):
        1/0


The reason for the failure with the full traceback will be saved to the log
file and will be visible in the terminal if you are in `debug mode <debug>`.

User Namespaces
---------------
`hutch_python.namespace.class_namespace` can be used to create your own object
groupings by type. This will find all objects loaded by hutch python plus all
objects in your global environment, and accumulate them if they match a given
type. You can explititly provide the type object or you can opt to provide a
string.

.. code-block:: python

    from hutch_python.namespace import class_namespace

    one = 1
    two = 2
    three = 3

    integers = class_namespace(int)


.. ipython:: python
    :suppress:

    from hutch_python.namespace import class_namespace

    one = 1
    two = 2
    three = 3

    integers = class_namespace(int)

.. ipython:: python

    integers.three
    list(integers)  # Iterate through namespace in alphabetical order
