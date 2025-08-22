from models.camelizer import BaseSchema


class PresignRequest(BaseSchema):
    filename: str
    content_type: str
    conversion_type: str
