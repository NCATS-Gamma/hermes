"""hermes server."""
import logging.config
import importlib.resources as pkg_resources
import yaml

from aiohttp import web

from hermes.views import index, fetch

logger = logging.getLogger('hermes')


def setup():
    """Set up app and logger."""
    # Set up default logger.
    with pkg_resources.open_text('hermes', 'logging.yaml') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

    # setup app
    app = web.Application()
    app.router.add_post('/run', index)
    app.router.add_get('/fetch/{job_id}', fetch)
    return app
