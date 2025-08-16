import logging
import os
from datetime import datetime
import fastapi

import bcrypt
import redis
from fastapi.exceptions import HTTPException
from google.auth.credentials import Credentials
from jose import jwt
from jose.exceptions import JWTError
import models.auth
from redis.backoff import ConstantBackoff
from redis.retry import Retry
from utils.pgsql import *
import google.oauth2.id_token
from google.auth.transport import requests as grequests

logger = logging.getLogger()
BCRYPT_EFF = os.environ["BCRYPT_EFF"]


def __init_redis(should_decode: bool = True, db: int = 0) -> redis.Redis:
    _host = os.environ.get("REDIS_HOST")
    _port = os.environ.get("REDIS_PORT")

    if _host is None or _port is None:
        logger.error(
            "REDIS_HOST or REDIS_PORT not set - using localhost:6379 as default parameters"
        )
        raise RuntimeError("REDIS_HOST or REDIS_PORT not set")

    r = redis.Redis(
        host=f"{_host}",
        port=int(_port),
        decode_responses=should_decode,
        db=0,
        retry=Retry(retries=3, backoff=ConstantBackoff(backoff=1)),
    )

    return r


async def save_temp_state(uuid: str, state: str) -> None:
    r = __init_redis()
    r.hset(uuid, "state", state)


def retrieve_temp_state(uuid: str):
    r = __init_redis()
    return r.hget(uuid, "state")


async def store_credentials(credentials: Credentials) -> bool:
    if credentials is None:
        raise ValueError("property 'credentials' cannot be of NoneType")

    r = __init_redis()

    return True


def get_credentials(request: fastapi.Request) -> models.auth.Credentials:
    if request is None:
        raise ValueError("property 'request' cannot be of NoneType")

    if request.headers is None:
        raise ValueError("property 'request.headers' cannot be of NoneType")

    access_token = request.headers.get("Authorization") or ""
    refresh_token = request.headers.get("x-refresh-token") or ""
    id_token = request.headers.get("x-id-token") or ""

    decoded_at = jwt.decode(
        access_token,
        os.environ.get("JWT_SECRET_KEY") or "",
        algorithms=[os.environ.get("JWT_ALGORITHM") or ""],
    )
    return models.auth.Credentials(
        access_token=access_token,
        refresh_token=refresh_token,
        id_token=id_token,
        access_token_expiry=decoded_at["claims"]["exp"],
        refresh_token_expiry=decoded_at["claims"]["exp"],
    )


def generate_credentials(username: str, email: str) -> models.auth.Credentials:
    now = datetime.now()
    at_expiry = datetime(
        now.year, now.month, now.day, now.hour + 4, now.minute, now.second
    ).timestamp()

    rt_expiry = datetime(
        now.year, now.month, now.day + 7, now.hour, now.minute, now.second
    ).timestamp()

    it_expiry = at_expiry

    at = {
        "claims": {
            "sub": username,
            "email": email,
            "exp": at_expiry,
            "type": "access",
        },
        "headers": {"alg": os.environ.get("JWT_ALGORITHM")},
        "key": os.environ.get("JWT_SECRET_KEY"),
    }

    rt = {
        "claims": {
            "sub": username,
            "email": email,
            "exp": rt_expiry,
            "type": "refresh",
        },
        "headers": {"alg": os.environ.get("JWT_ALGORITHM")},
        "key": os.environ.get("JWT_REFRESH_KEY"),
    }

    it = {
        "claims": {
            "sub": username,
            "email": email,
            "exp": it_expiry,
            "type": "oidc",
        },
        "headers": {"alg": os.environ.get("JWT_ALGORITHM")},
        "key": os.environ.get("JWT_OIDC_KEY"),
    }

    at = jwt.encode(claims=at["claims"], key=at["key"], algorithm=at["headers"]["alg"])
    rt = jwt.encode(claims=rt["claims"], key=rt["key"], algorithm=rt["headers"]["alg"])
    it = jwt.encode(claims=it["claims"], key=it["key"], algorithm=it["headers"]["alg"])

    return models.auth.Credentials(
        access_token=at,
        refresh_token=rt,
        id_token=it,
        access_token_expiry=int(at_expiry),
        refresh_token_expiry=int(rt_expiry),
    )


def check_password(plaintext: str, hashed: str) -> bool:
    is_correct = bcrypt.checkpw(plaintext.encode("utf-8"), hashed.encode("utf-8"))
    if not is_correct:
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    return True


def get_user_goauth2_details(id_token: str) -> models.db.User:
    payload = google.oauth2.id_token.verify_oauth2_token(
        id_token,
        grequests.Request(),
        os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
        clock_skew_in_seconds=60,
    )
