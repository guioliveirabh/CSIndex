import multiprocessing
import pathlib

import gunicorn.app.base
from gunicorn.six import iteritems
from django.core.handlers.wsgi import WSGIHandler

from .extract_data import DataExtractor


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    # copied from http://docs.gunicorn.org/en/latest/custom.html

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main(args):
    print('Args: {0}'.format(args))

    options = {
        'bind': '%s:%s' % (args.ip, str(args.port)),
        'workers': number_of_workers(),
    }
    data_extractor = DataExtractor(args.data_dir)
    data_extractor.run()
    print('=== Starting HTTP server ===')
    print('Waiting conections')
    StandaloneApplication(WSGIHandler(), options).run()
