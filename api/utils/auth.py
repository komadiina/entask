import logging
import os

import redis
from google.auth.credentials import Credentials
from redis.backoff import ConstantBackoff
from redis.retry import Retry

logger = logging.getLogger()


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
