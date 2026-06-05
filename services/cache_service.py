import hashlib
import json
import logging
import os
from typing import Callable, Optional

from dotenv import load_dotenv
from redis import Redis
from redis.exceptions import RedisError


load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

_redis_client: Optional[Redis] = None


def get_redis_client() -> Redis:
    global _redis_client

    if _redis_client is None:
        _redis_client = Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            db=int(os.getenv("REDIS_DB", "0")),
            decode_responses=True,
        )
    return _redis_client


def build_cache_key(namespace: str, *parts: object) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"{namespace}:{digest}"


def get_cached_value(cache_key: str, redis_client: Optional[Redis] = None) -> Optional[str]:
    try:
        client = redis_client or get_redis_client()
        cached_value = client.get(cache_key)
    except RedisError as exc:
        logger.warning("Redis cache read failed for key %s: %s", cache_key, exc)
        return None

    if cached_value is None:
        logger.info("Cache miss for key %s", cache_key)
        return None

    logger.info("Cache hit for key %s", cache_key)
    return cached_value


def set_cached_value(
    cache_key: str,
    value: str,
    ttl_seconds: int = DEFAULT_CACHE_TTL_SECONDS,
    redis_client: Optional[Redis] = None,
) -> None:
    try:
        client = redis_client or get_redis_client()
        if ttl_seconds > 0:
            client.setex(cache_key, ttl_seconds, value)
        else:
            client.set(cache_key, value)
        logger.info("Cached key %s with ttl_seconds=%s", cache_key, ttl_seconds)
    except RedisError as exc:
        logger.warning("Redis cache write failed for key %s: %s", cache_key, exc)


def get_or_set_cache(
    cache_key: str,
    value_factory: Callable[[], Optional[str]],
    ttl_seconds: int = DEFAULT_CACHE_TTL_SECONDS,
    redis_client: Optional[Redis] = None,
) -> Optional[str]:
    cached_value = get_cached_value(cache_key, redis_client=redis_client)
    if cached_value is not None:
        return cached_value

    value = value_factory()
    if value is not None:
        set_cached_value(cache_key, value, ttl_seconds=ttl_seconds, redis_client=redis_client)
    return value
