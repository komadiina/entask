from enum import Enum
from typing import Any, Dict

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class WorkflowStatus(str, Enum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class WSNotification(BaseSchema):
    type: str = "progress-update"
    status: WorkflowStatus
    client_id: str
    message: str
    data: Dict[str, Any] = {}
