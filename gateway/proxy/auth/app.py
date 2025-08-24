import logging
import os

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Request, Response
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests as grequests
from google.oauth2 import id_token
from jose import jwt
from jose.exceptions import JWTError

app = FastAPI()
logging.basicConfig(filename="auth.log", level=logging.INFO)
logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
SECRET_KEYS = {
    "id_token_secret": os.getenv("JWT_OIDC_KEY", ""),
    "access_token_secret": os.getenv("JWT_SECRET_KEY", ""),
}
ALGORITHM = os.getenv("JWT_ALGORITHM", "")
GOOGLE_KEYS_URL = os.getenv("GOOGLE_KEYS_URL", "")


async def validate(request: Request, credentials: dict) -> Response:
    if not credentials or not all(credentials.values()):
        return Response(
            status_code=401, content={"error": "Invalid credentials supplied."}
        )

    if is_cached(request, credentials):
        logger.info(
            f"Returning cached credentials for ${credentials["id_token"][:10]}..."
        )
        return Response(status_code=200)

    token = credentials["id_token"]
    payload = None
    try:
        payload = jwt.decode(
            credentials["id_token"],
            SECRET_KEYS["id_token_secret"],
            algorithms=[ALGORITHM],
        )
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
    except Exception as e:
        raise HTTPException(status_code=401, detail=e.__format__(""))

    if not payload:
        raise HTTPException(status_code=401, detail="Unauthorized")

    await cache_redis(request, credentials)
    request.state.user = payload

    return Response(status_code=200)


def is_cached(request: Request, credentials: dict) -> bool:
    r = redis.from_url(
        f"redis://{os.getenv('REDIS_HOST', "redis")}:{os.getenv('REDIS_PORT', 6379)}"
    )

    if credentials["id_token"] in r.keys(pattern="credentials:"):
        return True

    return False


async def cache_redis(request: Request, credentials: dict) -> None:
    r = redis.from_url(
        f"redis://{os.getenv('REDIS_HOST', "redis")}:{os.getenv('REDIS_PORT', 6379)}"
    )

    await r.set("credentials:", credentials["id_token"], ex=60)
    logger.info(f"Stored credentials for ${credentials['id_token'][:10]}...")
    return


@app.route("/authorize", methods=["GET", "POST", "OPTIONS", "HEAD", "PUT", "DELETE"])
async def authorize(request: Request):

    id_token = request.headers.get("x-id-token")
    refresh_token = request.headers.get("x-refresh-token")
    auth_header = request.headers.get("Authorization")

    access_token = auth_header.split(" ")[1] if auth_header is not None else None

    return await validate(
        request,
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "id_token": id_token,
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("AUTH_PROXY_PORT", 6201)))
