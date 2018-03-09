Starting a Session
==================

Quick-start
-----------

Run the ``xxxpython`` script in hutch ``xxx``'s directory to start a session.
You do not need a specific ``python`` environment to do this.

Hutch Directories
-----------------

Each hutch has its own ``hutch-python`` landing directory that facilitates
launching a session. You should use the central directory at
``/reg/g/pcds/pyps/apps/hutch-python/xxx`` if you are running an
experiment. This is a clone of the central
``https://github.com/pcdshub/xxx`` repository. You have the option to
clone this for debugging and development.

You do not need to have a ``Python`` environment set up to run out of this
landing directory. All of the environment configuration is done for you in the
launch scripts.

There are three launch scripts and one helper script: (replace ``xxx`` with your hutch name e.g.
``xpp`` or ``mfx``):

- ``xxxpython``: Main launch script.
                 Starts an ``ipython`` session with hutch's environment and
                 configured devices. If called with a script, runs that script
                 instead of starting an interactive session. This feature is
                 useful for scripts that need to rely on the hutch's configured
                 devices.
- ``xxxrun``: Script launcher for a clean environment.
              Runs a ``python`` script in the hutch's ``python`` environment,
              but does not load any hutch devices.
- ``xxxenv``: Environment setup script.
              Source this script to activate the hutch's ``python``
              environment.
- ``xxxversion``: Helper script to define which environment to use for the
                  hutch in the other three scripts.
