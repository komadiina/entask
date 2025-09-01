from typing import Any, Dict, Optional, Union

from models.camelizer import BaseSchema


class ConversionRequest(BaseSchema):
    type: str
    client_id: Optional[Union[str, int]] = None
    object_key: str
    token: Optional[str] | None = None
    additional: Optional[Dict[str, Any]] = {}
