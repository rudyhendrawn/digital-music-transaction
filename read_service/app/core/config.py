import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
	DATABASE_URL: str = "sqlite:///./chinook.db"
	REDIS_URL: str = "redis://localhost:6379/0"

settings = Settings()