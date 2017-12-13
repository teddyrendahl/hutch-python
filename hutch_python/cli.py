import os
import sys
import argparse

from .load_conf import load
from .log_setup import setup_logging


def setup_cli_env():
    # Parse the user's arguments
    parser = argparse.ArgumentParser(description='Launch LCLS Hutch Python')
    parser.add_argument('--cfg', required=True,
                        help='Configuration yaml file')
    args = parser.parse_args()

    # Make sure the hutch's directory is in the path
    sys.path.insert(0, os.getcwd())

    # Set up logging
    log_dir = os.path.join(os.path.dirname(args.cfg), 'logs')
    setup_logging(dir_logs=log_dir)

    # Load objects from the configuration file
    return load(args.cfg)
