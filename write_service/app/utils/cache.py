import redis.asyncio as redis
from app.core.config import settings

class RedisCache:
	def __init__(self):
		self.redis = None

	async def initialize(self):
		self.redis = await redis.from_url(settings.REDIS_URL)

	async def close(self):
		if self.redis:
			await self.redis.close()

	async def invalidate(self, key: str):
		await self.redis.delete(key)

redis_cache = RedisCache()