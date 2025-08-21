from fastapi import FastAPI, Request
import logging
import os

app = FastAPI()
logger = logging.getLogger(__name__)


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
