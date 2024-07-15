from app.db.mongodb import get_database
from app.models import MessageModel
from app.schemas import MessageCreate
from bson import ObjectId
from bson.errors import InvalidId
import logging

logger = logging.getLogger(__name__)

async def create_message(message: MessageCreate) -> MessageModel:
    message_dict = message.dict()
    db = get_database()
    result = await db["messages"].insert_one(message_dict)
    return MessageModel(id=result.inserted_id, **message_dict)

async def get_messages(limit: int = 100):
    messages = []
    db = get_database()
    try:
        cursor = db["messages"].find().sort("timestamp", -1).limit(limit)
        async for doc in cursor:
            messages.append(MessageModel(**doc))
        logger.info(f"Retrieved {len(messages)} messages")
    except Exception as e:
        logger.error(f"Error getting messages: {e}")
        raise
    return messages

async def get_message(message_id: str):
    try:
        object_id = ObjectId(message_id)
    except InvalidId:
        logger.warning(f"Invalid message ID: {message_id}")
        return None
    db = get_database()
    message = await db["messages"].find_one({"_id": object_id})
    if message:
        return MessageModel(**message)
    logger.info(f"Message not found: {message_id}")
    return None