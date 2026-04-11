import redis.asyncio as redis
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

class RedisCache:
    def __init__(self):
        self.redis = None
    
    async def connect(self):
        self.redis = await redis.from_url("redis://localhost:6379", decode_responses=True)

    async def get_cache(self, key: str):
        data = await self.redis.get(key)
        return json.loads(data) if data else None   
    
    async def set_cache(self, key: str, value: any, expire: int = 3600):
        await self.redis.set(key, json.dumps(value, cls=DecimalEncoder), ex=expire)

    async def delete_cache(self, key: str):
        await self.redis.delete(key)
    
    async def incr(self, key: str):
        return await self.redis.incr(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

redis_client = RedisCache()