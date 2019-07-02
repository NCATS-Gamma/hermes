"""hermes server."""
import logging.config
import pkg_resources
import yaml

from aiohttp import web

from hermes.routes import setup_routes

logger = logging.getLogger('hermes')


def setup():
    """Set up app and logger."""
    # Set up default logger.
    with open(pkg_resources.resource_filename('hermes', 'logging.yaml'), 'r') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

    # setup app
    app = web.Application()
    setup_routes(app)
    return app
