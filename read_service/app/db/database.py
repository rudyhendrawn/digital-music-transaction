from databases import Database
from app.core.config import settings

print(settings.DATABASE_URL)
database = Database(settings.DATABASE_URL)