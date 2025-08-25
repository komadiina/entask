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


class WSMessageType(Enum):
    WorkflowInterrupt = "workflow-interrupt"
    Notification = "notification"
    Error = "error"
    Other = "other"


class AckStatus(Enum):
    Ack = "ack"
    Nack = "nack"


class WFInterruptType(Enum):
    Abort = "abort"
    Pause = "pause"
    Resume = "resume"


class WebSocketClientInterrupt(BaseSchema):
    type: WSMessageType
    signal: WFInterruptType
    token: Union[str, None]


class WebSocketClientMessage(BaseSchema):
    type: WSMessageType
    content: Union[WebSocketClientInterrupt, Any]


class WebSocketInterruptResponse(BaseSchema):
    status: AckStatus
    error: Union[Any, None]


class WebSocketServerMessage(BaseSchema):
    data: Union[WebSocketInterruptResponse, Any]


# client --> server
TWSClientMessage = WebSocketClientMessage | WebSocketClientInterrupt

# server --> client
TWSServerMessage = WebSocketServerMessage | WebSocketInterruptResponse
