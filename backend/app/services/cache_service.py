import json
import hashlib
import time
from typing import Optional
from app.config import REDIS_URL

_redis_client = None
_memory_cache: dict[str, tuple[dict, float]] = {}


def _get_redis():
    global _redis_client
    if _redis_client is None and REDIS_URL:
        import redis
        _redis_client = redis.from_url(REDIS_URL)
    return _redis_client


def _make_key(prefix: str, content: str) -> str:
    h = hashlib.md5(content.encode()).hexdigest()
    return f"resume:{prefix}:{h}"


def get_cached(prefix: str, content: str) -> Optional[dict]:
    key = _make_key(prefix, content)
    r = _get_redis()
    if r:
        data = r.get(key)
        if data:
            return json.loads(data)
        return None
    entry = _memory_cache.get(key)
    if entry is None:
        return None
    data, expires = entry
    if time.time() > expires:
        del _memory_cache[key]
        return None
    return data


def set_cached(prefix: str, content: str, data: dict, ttl: int = 3600):
    key = _make_key(prefix, content)
    r = _get_redis()
    if r:
        r.setex(key, ttl, json.dumps(data, ensure_ascii=False))
    else:
        _memory_cache[key] = (data, time.time() + ttl)
