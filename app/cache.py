from __future__ import annotations
from typing import Optional
import redis
from uvicorn.logging import logging
import json
from datetime import datetime

logger = logging.getLogger("uvicorn.app")
# Sync редис клиент
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

def cache_get(key: str) -> Optional[str]:
    value = redis_client.get(key)
    if value is not None:
        logger.info(f"Cache HIT: {key}")
    else:
        logger.info(f"Cache MISS: {key}")
    return value

def cache_set(key: str, value: str, ttl: int) -> None:
    redis_client.set(key, value, ex=ttl)
    logger.info(f"Cache SET: {key} (TTL {ttl}s)")

def cache_delete(key: str) -> None:
    redis_client.delete(key)
    logger.info(f"Cache INVALIDATED: {key}")

def save_refresh_session(refresh_token: str, user_id: int, user_agent: str, expires_at: datetime):
    data = {
        "user_id": user_id,
        "user_agent": user_agent,
        "expires_at": expires_at.isoformat()
    }
    ttl = int((expires_at - datetime.utcnow()).total_seconds())
    if ttl > 0:
        cache_set(f"refresh:{refresh_token}", json.dumps(data), ttl)

def get_refresh_session(refresh_token: str):
    data = cache_get(f"refresh:{refresh_token}")
    if data:
        return json.loads(data)
    return None

def delete_refresh_session(refresh_token: str):
    cache_delete(f"refresh:{refresh_token}")

def get_user_sessions(user_id: int):
    # скан всех рефреш ключей (для /sessions)
    keys = redis_client.keys("refresh:*")
    sessions = []
    for key in keys:
        data = json.loads(redis_client.get(key))
        if data["user_id"] == user_id:
            sessions.append({
                "refresh_token": key.split(":", 1)[1],
                "user_agent": data["user_agent"],
                "created_at": None,  # можно добавить
                "expires_at": data["expires_at"]
            })
    return sessions
