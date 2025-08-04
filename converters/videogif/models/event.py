from pydantic import BaseModel
from typing import Dict, Any


class ConversionEvent(BaseModel):
    event_type: str
    data: Dict[str, Any]
