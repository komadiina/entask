from models.camelizer import BaseSchema


class User(BaseSchema):
    username: str
    email: str
    given_name: str
    family_name: str
    password: str | None
