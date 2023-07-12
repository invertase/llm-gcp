from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class Sender(Enum):
    USER = 1
    BOT = 2


class ChatMessage(BaseModel):
    sender: Sender
    message: str
    # default to now
    timestamp: datetime = Field(default_factory=datetime.now)
    id_token: str = None
    user_id: str = None
