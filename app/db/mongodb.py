from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    settings = settings

    def get_client(self) -> AsyncIOMotorClient:
        if self.client is None:
            try:
                self.client = AsyncIOMotorClient(self.settings.MONGODB_URL)
                logger.info("Created new connection to MongoDB")
            except Exception as e:
                logger.error(f"Error connecting to MongoDB: {e}")
                raise
        return self.client

    def get_db(self):
        return self.get_client()[self.settings.DATABASE_NAME]

db = Database()

async def connect_to_mongo():
    try:
        # Trigger connection to MongoDB
        db.get_client()
        logger.info("Connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    if db.client:
        db.client.close()
        db.client = None
        logger.info("Closed MongoDB connection")

def get_database():
    return db.get_db()