"""Core hermes functions."""
import asyncio
import hashlib
import json
import logging
import logging.config
import os

import aiohttp
import redis

logger = logging.getLogger('hermes')

CACHE_DIR = 'cache/'


async def run_job(body, job_id):
    """Run job."""
    logger.debug('Executing job %s...', job_id)
    message = body['message']
    message_id = hash_message(message)
    r = redis.Redis(decode_responses=True)
    async with aiohttp.ClientSession() as session:
        for action in body['actions']:
            step_id = get_job_id(message_id, action)
            if r.exists(step_id):
                logger.debug('Step %s is cached. Fetching...', step_id)
                message_id = r.get(step_id)
                continue
            url = action['url']
            options = action['options']
            inputs = {
                'message': message,
                'options': options
            }
            logger.debug('Step %s is not cached. Calling to %s...', step_id, url)
            async with session.post(url, json=inputs) as response:
                message_text = await response.text()
            message = json.loads(message_text)
            message_id = hash_message(message)
            r.set(step_id, message_id)
    r.set(job_id, message_id)
    with open(os.path.join(CACHE_DIR, message_id + '.json'), 'w') as f:
        json.dump(message, f, indent=4)


async def queue_job(arg):
    """Queue hermes job."""
    message = arg['message']
    actions = arg['actions']
    input_id = hash_message(message)
    job_id = get_job_id(input_id, actions)
    r = redis.Redis(decode_responses=True)
    if r.exists(job_id):
        output_id = r.get(job_id)
        logger.debug('Looking for message %s...', output_id)
        dir_contents = os.listdir(CACHE_DIR)
        filename = output_id + '.json'
        if filename in dir_contents:
            logger.debug('Result of job %s exists. Skipping...', job_id)
            return job_id

    logger.debug('Queueing execution of %s...', job_id)
    asyncio.create_task(run_job(arg, job_id))
    return job_id


def hash_string(string):
    """Hash string."""
    return hashlib.md5(string.encode('utf-8')).hexdigest()


def hash_message(message):
    """Hash message."""
    return hash_string(json.dumps(message))


def get_job_id(message_id, action):
    """Get job id."""
    if not isinstance(message_id, str):
        message_id = hash_message(message_id)
    return hash_string(message_id + json.dumps(action))
