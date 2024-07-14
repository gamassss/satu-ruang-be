from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    settings = settings

db = Database()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    print("Connected to database")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Closed database connection.")