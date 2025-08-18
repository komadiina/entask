from routers import auth
from routers.auth import get_user_details, oauth2, oauth2_callback

__all__ = ["oauth2", "oauth2_callback", "get_user_details", "auth"]
