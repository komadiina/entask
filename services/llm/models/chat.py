from typing import Optional

from models.camelizer import BaseSchema
from models.message import Message


class ChatRequest(BaseSchema):
    messages: list[Message]
    model: Optional[str] | None = None
