import logging
import os
from typing import List

from fastapi import APIRouter, FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from routers.auth import auth_router

logger = logging.getLogger()
app = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=[f"http://localhost:{os.environ.get('FRONTEND_PORT')}", "*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
)


@app.get("/api/version")
async def version():
    return {"version": os.environ.get("API_VERSION")}


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

    uvicorn.run(
        app=app, host="0.0.0.0", port=int(f"{os.environ.get("API_PORT")}") or 4201
    )
