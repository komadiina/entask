from typing import Optional, Union

from models.camelizer import BaseSchema


class ConversionRequest(BaseSchema):
    type: str
    user_id: Optional[Union[str, int]] = None
    object_key: str
