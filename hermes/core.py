"""Core hermes functions."""
import asyncio
import hashlib
import json
import logging
import logging.config
import os

import aiohttp

logger = logging.getLogger('hermes')

CACHE_DIR = 'cache/'


async def run_job(body, name):
    """Run job."""
    message = body['message']
    async with aiohttp.ClientSession() as session:
        for action in body['actions']:
            url = action['url']
            options = action['options']
            inputs = {
                'message': message,
                'options': options
            }
            logger.debug('Calling to %s...', url)
            print(f'Calling to {url}...')
            async with session.post(url, json=inputs) as response:
                print('Awaiting response...')
                message_text = await response.text()
                print('Got response.')
                message = json.loads(message_text)
    with open(os.path.join(CACHE_DIR, name + '.json'), 'w') as f:
        json.dump(message, f, indent=4)


async def queue_job(arg):
    """Queue hermes job."""
    # Compute job id
    job_id = hashlib.md5(json.dumps(arg).encode('utf-8')).hexdigest()

    # Check cache
    dir_contents = os.listdir(CACHE_DIR)
    filename = job_id + '.json'
    if filename in dir_contents:
        logger.debug('%s exists. Skipping...', job_id)
    else:
        logger.debug('Queueing execution of %s...', job_id)
        asyncio.create_task(run_job(arg, job_id))

    return job_id
