import os
import sys

import django
from django.core.management import call_command

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


def setup_django():
    os.environ["DJANGO_SETTINGS_MODULE"] = "csi.settings"
    django.setup(set_prefix=False)
    call_command('makemigrations', verbosity=0, interactive=False)
    call_command('migrate', verbosity=0, interactive=False)
    call_command('collectstatic', verbosity=0, interactive=False)


def entry_point():
    setup_django()

    from .main import main
    main()
