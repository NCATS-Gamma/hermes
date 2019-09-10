"""hermes server."""
import logging.config
import importlib.resources as pkg_resources
import os
import yaml

from aiohttp import web
import aiohttp_cors

from hermes.handlers import run, get_result, get_job

# Set up default logger.
with pkg_resources.open_text('hermes', 'logging.yml') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)

# setup app
app = web.Application()
app.router.add_post('/run', run)
app.router.add_get('/result/{job_id}', get_result)
app.router.add_get('/job/{job_id}', get_job)

if os.environ.get('USE_CORS', False):
    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)
