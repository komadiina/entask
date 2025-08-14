from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt
import requests
import os
from constants.paths import PUBLIC_PATHS

# your app secret
SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or ""
ALGORITHM = os.environ.get("JWT_ALGORITHM") or ""

# Google public keys URL
GOOGLE_KEYS_URL = "https://www.googleapis.com/oauth2/v3/certs"
_google_keys = None

VERSION = os.environ.get("API_VERSION")


def get_google_keys():
    global _google_keys
    if _google_keys is None:
        r = requests.get(GOOGLE_KEYS_URL)
        _google_keys = r.json()["keys"]
    return _google_keys


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # skip auth for public routes
        if request.url.path.startswith(
            f"/api/{VERSION}/public"
        ) or request.url.path.startswith(f"/api/public/version"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing auth token")
        token = auth_header.split(" ")[1]

        payload = None
        try:
            # entask-issued token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except RuntimeError:
            # Google-issued token
            keys = get_google_keys()
            for key in keys:
                try:
                    payload = jwt.decode(
                        token,
                        key=key,
                        algorithms=["RS256"],
                        audience="YOUR_GOOGLE_CLIENT_ID",
                    )
                    break
                except RuntimeError:
                    continue

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        # optionally attach payload to request.state.user
        request.state.user = payload
        return await call_next(request)
