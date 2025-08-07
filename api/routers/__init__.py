from routers import auth
from routers.auth import oauth2, oauth2_callback, get_user_details

__all__ = ["oauth2", "oauth2_callback", "get_user_details", "auth"]
