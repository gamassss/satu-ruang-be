from fastapi import APIRouter, HTTPException
from app.schemas import MessageCreate, MessageResponse
from app.services import create_message, get_messages, get_message

router = APIRouter()

@router.post("/messages/", response_model=MessageResponse)
async def post_message(message: MessageCreate):
    created_message = await create_message(message)
    return MessageResponse(
        id=str(created_message.id),
        content=created_message.content,
        sender=created_message.sender,
        timestamp=created_message.timestamp
    )

@router.get("/messages/", response_model=list[MessageResponse])
async def list_messages(limit: int=100):
    messages = await get_messages(limit)
    return [MessageResponse(
        id=str(msg.id),
        content=msg.content,
        sender=msg.sender,
        timestamp=msg.timestamp
    ) for msg in messages]

@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_single_message(message_id: str):
    message = await get_message(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message Not Found")
    return MessageResponse(
        id=str(message.id),
        content=message.content,
        sender=message.sender,
        timestamp=message.timestamp
    )