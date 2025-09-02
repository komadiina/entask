from typing import Any, List, Optional, Union, Dict

from models.camelizer import BaseSchema


class ConversionRequest(BaseSchema):
    type: str
    client_id: Optional[Union[str, int]] = None
    object_key: str
    token: Optional[str] | None = None
    additional: Optional[List[Dict[str, Any]]] = []
