"""Views."""
import functools
import json
import logging
import os

from aiohttp import web
import redis

from hermes.core import queue_job, CACHE_DIR

logger = logging.getLogger('hermes')


async def index(request):
    """Index view."""
    body = await request.json()
    job_id = await queue_job(body)
    return web.Response(text=job_id)


async def fetch(request):
    """Fetch-message endpoint."""
    job_id = request.match_info['job_id']
    r = redis.Redis(decode_responses=True)
    if not r.exists(job_id):
        return web.HTTPNotFound(text='Results are unavailable.')
    output_id = r.get(job_id)
    filename = output_id + '.json'
    try:
        with open(os.path.join(CACHE_DIR, filename), 'r') as f:
            response = json.load(f)
    except FileNotFoundError:
        return web.HTTPNotFound(text='Results are unavailable.')
    return web.json_response(response, dumps=functools.partial(json.dumps, indent=4))
