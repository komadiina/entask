from typing import Optional

from models.camelizer import BaseSchema


class RegisterRequestModel(BaseSchema):
    given_name: str
    family_name: str
    email: str
    email_confirmed: str
    # picture_url: str
    username: str
    password: str
    password_confirmed: str

    def is_incomplete(self) -> bool:
        if (
            self.given_name is None
            or self.family_name is None
            or self.email is None
            or self.email_confirmed is None
        ):
            return True

        elif self.email != self.email_confirmed:
            return True

        return False


class LoginRequestModel(BaseSchema):
    username_email: str
    password: str


class Credentials(BaseSchema):
    access_token: str
    refresh_token: str
    id_token: str
    token_type: str = "bearer"
    access_token_expiry: int
    refresh_token_expiry: int
    provider: str = "entask"
    uuid: Optional[str] = None
