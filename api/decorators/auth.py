import os

import requests
from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyHeader
from fastapi_decorators import depends
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests as grequests
from google.oauth2 import id_token
from jose import jwt
from jose.exceptions import JWTError

# your app secret
SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or ""
ALGORITHM = os.environ.get("JWT_ALGORITHM") or ""

# Google public keys URL
GOOGLE_KEYS_URL = os.environ.get("GOOGLE_KEYS_URL") or ""
_google_keys = None

VERSION = os.environ.get("API_VERSION")


def get_google_keys():
    global _google_keys
    if _google_keys is None:
        r = requests.get(GOOGLE_KEYS_URL)
        _google_keys = r.json()["keys"]
    return _google_keys


oauth2_scheme = APIKeyHeader(name="g-id-token", auto_error=False)


def auth_dependency(request: Request, token: str = Depends(oauth2_scheme)):
    """
      JWT authentication flow (Google OAuth2, Entask-issued).

    Args:
        request (Request): The client request.
        token (str, optional): The supplied token in request headers ('g-id-token'). Defaults to Depends(oauth2_scheme).

    Raises:
        HTTPException: If 'token' is not supplied in payload, or is invalid.
    """
    payload = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        try:
            payload = id_token.verify_oauth2_token(
                token,
                grequests.Request(),
                os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
                clock_skew_in_seconds=60,
            )
        except ValueError or GoogleAuthError as e:
            payload = None

    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")

    request.state.user = payload


authorized = depends(auth_dependency)
"""
  Authorization decorator - see `decorators.auth.auth_dependency` for more information.
"""
