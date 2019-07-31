"""Test hermes."""
import pytest
from aiohttp import web
from hermes.server import setup
from hermes.core import run_job, get_job_id


async def plus(request):
    """Plus request handler."""
    request_json = await request.json()
    message = request_json['message']
    message['value'] += request_json['options'].get('value', 1)
    return web.json_response(message)


@pytest.fixture
def cli(loop, aiohttp_client):
    """Test server."""
    app = setup()
    app.router.add_post('/plus', plus)
    return loop.run_until_complete(aiohttp_client(app))


async def test_hermes(cli):
    """Test hermes."""
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
            },
            {
                'url': f'http://{cli.server.host}:{cli.server.port}/plus',
                'options': {
                    'value': 2
                }
            }
        ]
    }

    # run job
    job_id = get_job_id(test_input['message'], test_input['actions'])
    await run_job(test_input, job_id)

    # call /run endpoint - job should exist and be skipped
    response = await cli.post('/run', json=test_input)
    job_id = await response.text()

    # fetch result
    response = await cli.get(f'/result/{job_id}')

    assert response.status == 200
    result = await response.json()

    assert result['value'] == 3
