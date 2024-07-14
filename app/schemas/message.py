from pydantic import BaseModel, Field
from datetime import datetime

class MessageCreate(BaseModel):
    content: str
    sender: str
    timestamp: datetime = Field(default_factory=datetime.now)

class MessageResponse(BaseModel):
    id: str
    content: str
    sender: str
    timestamp: datetime

    class Config:
        form_attributes = True