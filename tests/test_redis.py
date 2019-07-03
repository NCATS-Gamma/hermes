"""Test redis."""
import redis


def test_redis():
    """Test redis."""
    r = redis.Redis(decode_responses=True)
    r.set('foo', 'bar')
    assert r.get('foo') == 'bar'
