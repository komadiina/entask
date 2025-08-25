from models.camelizer import BaseSchema
from typing import Dict, Any, Optional, Union


class WebSocketMessage(BaseSchema):
    message: str
    data: Optional[Union[Dict[str, Any], str]] = None
