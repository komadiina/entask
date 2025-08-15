import logging
import os

import redis
from datetime import timedelta
from google.auth.credentials import Credentials
from redis.backoff import ConstantBackoff
from redis.retry import Retry
from models.auth import LoginRequestModel, Credentials
from utils.pgsql import *
from jose import jwt
from jose.exceptions import JWTClaimsError, JWTError, ExpiredSignatureError
import bcrypt

logger = logging.getLogger()
BCRYPT_EFF = 16


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


def generate_credentials(user: LoginRequestModel) -> Credentials:
    at_expiry = timedelta(minutes=60)
    rt_expiry = timedelta(days=7)
    at = {
        "claims": {
            "sub": user.username_email,
            "email": user.username_email,
            "exp": at_expiry,
        },
        "headers": {"alg": os.environ.get("JWT_ALGORITHM")},
        "key": os.environ.get("JWT_SECRET_KEY"),
    }
    rt = {**at}
    rt["claims"]["exp"] = rt_expiry

    at = jwt.encode(claims=at["claims"], key=at["key"], algorithm=at["headers"]["alg"])
    rt = jwt.encode(claims=rt["claims"], key=rt["key"], algorithm=rt["headers"]["alg"])
    return Credentials(
        access_token=at,
        refresh_token=rt,
        id_token=at,
        access_token_expiry=at_expiry,
        refresh_token_expiry=rt_expiry,
    )


def check_password(plaintext: str, hashed: str) -> bool:
    return bcrypt.checkpw(plaintext.encode("utf-8"), hashed.encode("utf-8"))
