from enum import Enum

from models.camelizer import BaseSchema


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseSchema):
    content: str
    role: Role = Role.USER
