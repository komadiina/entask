from typing import Optional

from models.camelizer import BaseSchema
from models.message import Message, Role


class ChatRequest(BaseSchema):
    messages: list[Message]
    model: Optional[str] = None
