import logging
import os

import redis
from fastapi.exceptions import HTTPException
from google.auth.credentials import Credentials
from redis.backoff import ConstantBackoff
from redis.retry import Retry
from models.auth import RegisterRequestModel, LoginRequestModel
from utils.pgsql import *
from typing import Dict, Any
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


def register_user(user: RegisterRequestModel) -> Dict[str, Any]:
    # open pgsql connection
    conn = get_connection()
    cur = get_cursor(conn)

    # check if user already exists (username && email criteria)
    cur = cur.execute(
        query="SELECT * FROM users WHERE username = %s OR email = %s;",
        params=(user.username, user.email),
    )
    result = cur.fetchall()
    if len(result) > 0:
        raise HTTPException(status_code=400, detail="User already exists")

    # save into pgsql 'users' table
    cur = cur.execute(
        query="INSERT INTO users (username, email, given_name, family_name, password) VALUES (%s, %s, %s, %s, %s);",
        params=(
            user.username,
            user.email,
            user.given_name,
            user.family_name,
            bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt(BCRYPT_EFF)),
        ),
    )
    conn.commit()
    close_cursor(cur)
    close_connection(conn)

    return {"message": "User registered successfully"}


def check_login(user: LoginRequestModel):
    # open pgsql connection
    conn = get_connection()
    cur = get_cursor(conn)

    # check if user already exists (username && email criteria)
    cur = cur.execute(
        query="SELECT * FROM users WHERE username = %s OR email = %s;",
        params=(user.username_email, user.username_email),
    )
    result = cur.fetchall()
    if len(result) > 0:
        for row in result:
            if check_password(user.password, row["password"]):
                return generate_token(user)
    else:
        raise HTTPException(status_code=400, detail="User does not exist")


def generate_token(user: LoginRequestModel):
    return {"accessToken": "token", "refreshToken": "token"}


def check_password(plaintext: str, hashed: str) -> bool:
    return bcrypt.checkpw(plaintext.encode("utf-8"), hashed.encode("utf-8"))
