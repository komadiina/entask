import datetime
import logging
import os
from typing import List

from fastapi import APIRouter, FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from routers.auth import auth_router

logging.basicConfig(filename=f"logs/{datetime.datetime.now()}.log", level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=[f"http://localhost:{os.environ.get('FRONTEND_PORT')}", "*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
    docs_url="/api/auth/docs",
    openapi_url="/api/auth/openapi.json",
    redoc_url="/api/auth/redoc",
)


@app.get("/api/auth/health", status_code=200)
async def health():
    return {"status": "ok"}


@app.get("/api/auth/version")
async def version():
    return {"service": "auth-service", "version": os.environ.get("AUTH_API_VERSION")}


def __init_app(app: FastAPI, routers: List[APIRouter]) -> FastAPI:
    for router in routers:
        app.include_router(router)
    return app


if __name__ == "__main__":
    import uvicorn

    # TODO: testing - didnt setup ssl/tls on dev yet, [[REMOVE]] in prod
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

    included_routers = [auth_router]

    __init_app(app, included_routers)

    uvicorn.run(app=app, host="0.0.0.0", port=int(os.getenv("AUTH_SERVICE_PORT", 5201)))
