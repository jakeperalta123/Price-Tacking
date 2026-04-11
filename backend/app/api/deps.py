def get_redis():
    from app.core.redis import redis_client
    return redis_client