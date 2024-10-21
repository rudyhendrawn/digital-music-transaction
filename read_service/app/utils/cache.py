import redis.asyncio as redis
import pickle
from functools import wraps
from app.core.config import settings
from typing import Callable, Any, Coroutine

class RedisCache:
	def __init__(self):
		self.redis = None

	async def initialize(self):
		print(settings.REDIS_URL)
		self.redis = await redis.from_url(settings.REDIS_URL)

	async def close(self):
		if self.redis:
			await self.redis.close()

redis_cache = RedisCache()

def cache(expire: int = 60):
	def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
		@wraps(func)
		async def wrapper(*args, **kwargs):
			key = f"{func.__name__}:{args}:{kwargs}"
			cached_result = await redis_cache.redis.get(key)
			if cached_result:
				return pickle.loads(cached_result)
			result = await func(*args, **kwargs)
			await redis_cache.redis.set(key, pickle.dumps(result), ex=expire)
			return result
		return wrapper
	return decorator