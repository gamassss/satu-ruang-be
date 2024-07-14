from app.db.mongodb import db
from app.models import MessageModel
from app.schemas import MessageCreate
from bson import ObjectId
from bson.errors import InvalidId

async def create_message(message: MessageCreate) -> MessageModel:
    message_dict = message.dict()
    result = await db.client[db.settings.DATABASE_NAME]["messages"].insert_one(message_dict)
    return MessageModel(id=result.inserted_id, **message_dict)

async def get_messages(limit: int = 100):
    messages = []
    cursor = db.client[db.settings.DATABASE_NAME]["messages"].find().sort("timestamp", -1).limit(limit)
    async for doc in cursor:
        messages.append(MessageModel(**doc))

    return messages

async def get_message(message_id: str):
    try:
        object_id = ObjectId(message_id)
    except InvalidId:
        return None
    message = await db.client[db.settings.DATABASE_NAME]["messages"].find_one({"_id": object_id})
    if message:
        return MessageModel(**message)
    return None