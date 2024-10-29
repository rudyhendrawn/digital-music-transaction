import logging
from fastapi import FastAPI
from app.api.routes import router
from app.db.database import database
from app.utils.cache import redis_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Write Transaction Service")

app.include_router(router)

@app.on_event("startup")
async def startup():
	try:
		await database.connect()
		logger.info("	Successfully connected to SQLite database")
	except Exception as e:
		logger.error(f"	Failed to connect to SQLite database: {e}")

	try:
		await redis_cache.initialize()
		logger.info("	Successfully connected to Redis")
	except Exception as e:
		logger.error(f"	Failed to connect to Redis: {e}")

@app.on_event("shutdown")
async def shutdown():
	await database.disconnect()
	await redis_cache.close()