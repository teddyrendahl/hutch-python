import os
import sys
import argparse

from IPython.terminal.embed import (InteractiveShellEmbed,
                                    load_default_config)

from .ipython_log import init_ipython_logger
from .load_conf import load
from .log_setup import setup_logging
from .plugins import hutch


def setup_cli_env():
    # Parse the user's arguments
    parser = argparse.ArgumentParser(description='Launch LCLS Hutch Python')
    parser.add_argument('--cfg', required=True,
                        help='Configuration yaml file')
    parser.add_argument('--db', required=True,
                        help='Device database access information')
    args = parser.parse_args()

    # Make sure the hutch's directory is in the path
    sys.path.insert(0, os.getcwd())

    # Set up logging
    log_dir = os.path.join(os.path.dirname(args.cfg), 'logs')
    setup_logging(dir_logs=log_dir)

    # Set the happi db path
    hutch.HAPPI_DB = args.db

    # Load objects from the configuration file
    return load(args.cfg)


def hutch_ipython_embed():
    """
    This is very hacky, but I couldn't find a better way to adjust the shell
    from a call to embed.
    """
    config = load_default_config()
    config.InteractiveShellEmbed = config.TerminalInteractiveShell
    frame = sys._getframe(1)
    shell = InteractiveShellEmbed.instance(_init_location_id='%s:%s' % (
        frame.f_code.co_filename, frame.f_lineno), config=config)
    init_ipython_logger(shell)
    shell(header=u'', stack_depth=2, compile_flags=None,
          call_location_id='%s:%s' % (frame.f_code.co_filename,
                                      frame.f_lineno))
