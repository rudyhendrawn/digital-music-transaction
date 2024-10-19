import os

class Settings:
	PROJECT_NAME: str = "Read Service"
	PROJECT_VERSION: str = "1.0.0"
	PROJECT_DESCRIPTION: str = "Read Service"
	PROJECT_ROOT: str = os.path.dirname(os.path.abspath(__file__))
	API_V1_STR: str = "/api/v1"
	SECRET_KEY: str = "c2e1b6f4b3e"
	ACCESS_TOKEN = "c2e1b6f4b3e"
	REFRESH_TOKEN = "c2e1b6f4b3e"
	DATABASE_URL: str = "sqlite:///./chinook.db"
	REDIS_URL: str = "redis:///redis-16824.c252.ap-southeast-1-1.ec2.redns.redis-cloud.com:16824"
	REDIS_PASSWORD: str = "HAdS2NjvY2BxlUCvX8GcVYBA97Xb3WP6"

settings = Settings()