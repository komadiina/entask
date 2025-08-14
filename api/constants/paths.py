import os

VERSION = os.environ.get("API_VERSION")
PUBLIC_PATHS = [
    f"/api/{VERSION}/auth/oauth2",
    f"/api/{VERSION}/auth/oauth2/callback",
    f"/api/{VERSION}/auth/register",
    f"/api/{VERSION}/auth/login",
]
