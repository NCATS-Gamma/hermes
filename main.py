"""Main."""
from aiohttp import web
from hermes.server import app


web.run_app(app, port=8081)
