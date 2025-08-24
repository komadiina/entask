from models.camelizer import BaseSchema


class ConversionRequest(BaseSchema):
    type: str
    user_id: str | int
    object_key: str
