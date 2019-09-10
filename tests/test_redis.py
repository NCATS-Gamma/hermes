"""Test redis."""
import os
import redis


def test_redis():
    """Test redis."""
    r = redis.Redis(
        host=os.environ['REDIS_HOST'],
        port=6379,
        decode_responses=True,
    )
    r.set('foo', 'bar')
    assert r.get('foo') == 'bar'
