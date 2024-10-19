from fastapi import FastAPI
from app.api.routes import router
from app.db.database import database
from app.utils.cache import redis_cache

app = FastAPI(title="Read and Search Transaction Service")

app.include_router(router)

@app.on_event("startup")
async def startup():
	await database.connect()
	await redis_cache.initialize()
	app.state.redis = redis_cache

@app.on_event("shutdown")
async def shutdown():
	await database.disconnect()
	await app.state.redis.close()