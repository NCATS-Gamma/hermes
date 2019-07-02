"""Main."""
from aiohttp import web
from hermes.server import setup


web.run_app(setup(), port=8081)
