import logging
import os

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from routers.convert import convert_router

NATS_USER = os.getenv("NATS_USER")
NATS_PASSWORD = os.getenv("NATS_PASSWORD")
# NATS_HOST = os.getenv("NATS_HOST", "nats-1")
NATS_CLIENT_PORT = int(os.getenv("NATS_CLIENT_PORT", 4222))

HOSTS = ["nats-1", "nats-2", "nats-3"]

logging.basicConfig(filename="conversion-service.log", level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    docs_url="/api/conversion/docs",
    openapi_url="/api/conversion/openapi.json",
    redoc_url="/api/conversion/redoc",
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
)
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
