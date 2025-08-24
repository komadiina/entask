from typing import Any, Dict

from pydantic import BaseModel


class ConversionEvent(BaseModel):
    event_type: str
    data: Dict[str, Any]
