from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    content: str
    sender: str

class MessageResponse(BaseModel):
    id: str
    content: str
    sender: str
    timestamp: datetime

    class Config:
        form_attributes = True