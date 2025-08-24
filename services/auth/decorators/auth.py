import json
import logging
import os

from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyHeader
from fastapi_decorators import depends
from google.auth.transport import requests as grequests
from google.oauth2 import id_token
from jose import jwt
from redis.asyncio import Redis

JWT_OIDC_KEY = os.getenv("JWT_OIDC_KEY", "")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "")

logging.basicConfig(filename="auth.log", level=logging.INFO)
logger = logging.getLogger(__name__)
auth_token = APIKeyHeader(name="x-id-token", auto_error=False)

r = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True,
)


async def auth_dependency(request: Request, token: str = Depends(auth_token)):
    """
      JWT authentication flow (Google OAuth2, Entask-issued).

    Args:
        request (Request): The client request.
        token (str, optional): The supplied token in request headers ('g-id-token'). Defaults to Depends(oauth2_scheme).

    Raises:
        HTTPException: If 'token' is not supplied in payload, or is invalid.
    """
    # check if cached in redis
    payload = None
    cached = None
    if token is not None:
        cached = await r.get(token)

    if cached:
        payload = json.loads(cached)
        request.state.user = payload
        return

    if request.headers.get("x-auth-type") == "google":
        logger.info("Using Google OAuth2 identification flow")
        try:
            payload = id_token.verify_oauth2_token(
                token,
                grequests.Request(),
                os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
                clock_skew_in_seconds=60,
            )
        except:
            raise HTTPException(status_code=401, detail="Unauthorized")

    else:
        logger.info("Using Entask identification flow")
        try:
            payload = jwt.decode(token, JWT_OIDC_KEY, algorithms=[JWT_ALGORITHM])
        except Exception as e:
            raise HTTPException(status_code=401, detail=e.__format__(""))

    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # cache token for 5 minutes
    await r.setex(token, 300, json.dumps(payload))

    request.state.user = payload


authorized = depends(auth_dependency)
"""
  Authorization decorator - see `decorators.auth.auth_dependency` for more information.
"""
