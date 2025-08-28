from enum import Enum
from typing import Any, Union

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class InterruptType(Enum):
    ABORT = "abort"
    PAUSE = "pause"
    RESUME = "resume"


class WebSocketClientInterrupt(BaseSchema):
    user_id: str
    workflow_id: str
    interrupt_type: InterruptType


class ResponseType(str, Enum):
    UPDATE = "progress-update"
    ACK = "ack"
    ERROR = "error"
    OTHER = "other"


class WebSocketResponse(BaseSchema):
    type: ResponseType
    client_id: str
    status: str
    message: str
    data: Any
