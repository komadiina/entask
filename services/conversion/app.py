import logging
import os
from contextlib import asynccontextmanager
from typing import cast

import nats
from fastapi import FastAPI
from nats.aio.client import Client as NATSClient

NATS_USER = os.getenv("NATS_USER")
NATS_PASSWORD = os.getenv("NATS_PASSWORD")
NATS_HOST = os.getenv("NATS_HOST", "0.0.0.0")
NATS_CLIENT_PORT = int(os.getenv("NATS_CLIENT_PORT", 4222))
NATS_CONNINFO = "nats://{}:{}@{}:{}".format(
    NATS_USER, NATS_PASSWORD, NATS_HOST, NATS_CLIENT_PORT
)


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup, initialize nats_client for this service instance
    app.state.nats_client = cast(NATSClient, await nats.connect(NATS_CONNINFO))
    yield

    # shutdown, close the nats connection
    await app.state.nats_client.close()


app = FastAPI(lifespan=lifespan)


@app.get("/conversion/health")
async def health():
    return {"status": "ok"}


@app.get("/conversion/version")
async def version():
    return {
        "service": "conversion-service",
        "version": os.getenv("CONVERSION_API_VERSION", "v1"),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host="0.0.0.0", port=int(os.getenv("CONVERSION_SERVICE_PORT", 5203))
    )
