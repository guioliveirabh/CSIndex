import argparse
import logging
import pathlib
import os
import sys

import django
from django.core.management import call_command

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


def parse_args():
    def real_path(path):
        path = pathlib.Path(path).resolve()
        if not path.is_dir():
            raise argparse.ArgumentError(message='A valid directory must be provided')

        return path

    parser = argparse.ArgumentParser(description='CSIndex REST API server')
    parser.add_argument('-i', '--ip', metavar='IP', default='127.0.0.1', help='the bind IP')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default='8000', help='the bind port')
    parser.add_argument('-d', '--data-dir', metavar='DIRECTORY', type=real_path, required=True,
                        help='the CSV files directory')

    return parser.parse_args()


def setup_django():
    args = parse_args()

    os.environ["DJANGO_SETTINGS_MODULE"] = "csi.settings"
    django.setup(set_prefix=False)
    call_command('makemigrations', verbosity=0, interactive=False)
    call_command('migrate', verbosity=0, interactive=False)
    call_command('collectstatic', verbosity=0, interactive=False)

    logging.disable(logging.CRITICAL)

    return args


def entry_point():
    args = setup_django()

    from .main import main
    main(args)
