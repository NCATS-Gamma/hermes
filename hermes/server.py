"""hermes server."""
import logging.config
import importlib.resources as pkg_resources
import yaml

from aiohttp import web

from hermes.handlers import run, get_result, get_job

# Set up default logger.
with pkg_resources.open_text('hermes', 'logging.yaml') as f:
    config = yaml.safe_load(f.read())
logging.config.dictConfig(config)

# setup app
app = web.Application()
app.router.add_post('/run', run)
app.router.add_get('/result/{job_id}', get_result)
app.router.add_get('/job/{job_id}', get_job)
