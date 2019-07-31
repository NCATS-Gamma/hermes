"""Test hermes."""
import asyncio
import copy
import os
import pytest
import redis
from aiohttp import web
from hermes.server import app
from hermes.core import run_job, get_job_id, CACHE_DIR


async def plus(request):
    """Plus request handler."""
    request_json = await request.json()
    message = request_json['message']
    message['value'] += request_json['options'].get('value', 1)
    return web.json_response(message)


@pytest.fixture
def cli(loop, aiohttp_client):
    """Test server."""
    _app = copy.deepcopy(app)
    _app.router.add_post('/plus', plus)
    return loop.run_until_complete(aiohttp_client(_app))


async def test_hermes(cli):
    """Test hermes."""
    # generate 1-action job
    test_input = {
        'message': {
            'value': 0
        },
        'actions': [
            {
                'url': f'http://{cli.server.host}:{cli.server.port}/plus',
                'options': {
                    'value': 1
                }
            }
        ]
    }

    # run 1-action job
    response = await cli.post('/run', json=test_input)
    job_id = await response.text()

    # wait for job to finish
    r = redis.Redis(decode_responses=True)
    while r.get(job_id) is None:
        await asyncio.sleep(1)

    # add second action
    test_input['actions'].append({
        'url': f'http://{cli.server.host}:{cli.server.port}/plus',
        'options': {
            'value': 2
        }
    })

    # run 2-action job
    response = await cli.post('/run', json=test_input)
    job_id = await response.text()

    # wait for job to finish
    r = redis.Redis(decode_responses=True)
    while r.get(job_id) is None:
        await asyncio.sleep(0.1)

    # run job again - should be skipped
    response = await cli.post('/run', json=test_input)
    job_id = await response.text()

    # fetch result
    response = await cli.get(f'/result/{job_id}')

    # validate result
    assert response.status == 200
    result = await response.json()
    assert result['value'] == 3


async def test_missing(cli):
    """Test fetching missing result."""
    response = await cli.get(f'/result/nope')
    assert response.status == 404


async def test_lost(cli):
    """Test fetching lost result."""
    test_input = {
        'message': {
            'value': 0
        },
        'actions': [
            {
                'url': f'http://{cli.server.host}:{cli.server.port}/plus',
                'options': {
                    'value': 1
                }
            }
        ]
    }

    # run job
    job_id = get_job_id(test_input['message'], test_input['actions'])
    await run_job(test_input, job_id)

    # remove result file
    r = redis.Redis(decode_responses=True)
    result_id = r.get(job_id)
    os.remove(os.path.join(CACHE_DIR, result_id + '.json'))

    response = await cli.get(f'/result/{job_id}')
    assert response.status == 404
