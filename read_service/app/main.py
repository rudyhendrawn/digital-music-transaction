import logging
from fastapi import FastAPI
from app.api.routes import router
from app.db.database import database
from app.utils.cache import redis_cache

app = FastAPI(title="Read and Search Transaction Service")

app.include_router(router)

@app.on_event("startup")
async def startup():
	try:
		await database.connect()
		logging.info("	Successfully connected to SQLite database")
	except Exception as e:
		logging.error(f"	Failed to connect to SQLite database: {e}")

	try:
		await redis_cache.initialize()
		app.state.redis = redis_cache
		logging.info("	Successfully connected to Redis database")
	except Exception as e:
		logging.error(f"	Failed to connect to Redis database: {e}")


@app.on_event("shutdown")
async def shutdown():
	await database.disconnect()
	await app.state.redis.close()