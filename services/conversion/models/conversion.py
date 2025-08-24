from models.camelizer import BaseSchema


class ConversionRequest(BaseSchema):
    type: str
    user_id: str
    object_key: str
