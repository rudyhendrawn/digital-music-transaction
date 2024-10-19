import os

class Settings:
	PROJECT_NAME: str = "Write Service"
	PROJECT_VERSION: str = "1.0.0"
	PROJECT_DESCRIPTION: str = "Write Service"
	PROJECT_ROOT: str = os.path.dirname(os.path.abspath(__file__))
	API_V1_STR: str = "/api/v1"
	SECRET_KEY: str = "c2e1b6f4b3e"
	ACCESS_TOKEN = "c2e1b6f4b3e"
	REFRESH_TOKEN = "c2e1b6f4b3e"
	DATABASE_URL: str = "sqlite:///./chinook.db"

settings = Settings()