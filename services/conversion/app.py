import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import cast

import nats
from fastapi import FastAPI
from nats.aio.client import Client as NATSClient
from routers.convert import convert_router

NATS_USER = os.getenv("NATS_USER")
NATS_PASSWORD = os.getenv("NATS_PASSWORD")
# NATS_HOST = os.getenv("NATS_HOST", "nats-1")
NATS_CLIENT_PORT = int(os.getenv("NATS_CLIENT_PORT", 4222))

HOSTS = ["nats-1", "nats-2", "nats-3"]

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    nc = await nats.connect(
        servers=[
            "nats://{}:{}@{}:{}".format(
                NATS_USER, NATS_PASSWORD, host, NATS_CLIENT_PORT
            )
            for host in HOSTS
        ],
        verbose=True,
    )
    await nc.jetstream().add_stream(
        name="convert", subjects=["convert.*"], storage="file"
    )
    app.state.nats_client = nc

    try:
        yield
    finally:
        # graceful shutdown
        await nc.drain()
        await nc.close()


app = FastAPI(docs_url="/api/conversion/docs", lifespan=lifespan)
app.include_router(convert_router)


@app.get("/api/conversion/health")
async def health():
    return {"status": "ok"}


@app.get("/api/conversion/version")
async def version():
    return {
        "service": "conversion-service",
        "version": os.getenv("CONVERSION_API_VERSION", "v1"),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host="0.0.0.0", port=int(os.getenv("CONVERSION_SERVICE_PORT", 5205))
    )
