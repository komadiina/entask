import logging
import os

from fastapi import FastAPI, Request

app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/user-details/health")
async def health():
    return {"status": "ok"}


@app.get("/user-details/version")
async def version():
    return {"service": "user-service", "version": os.environ.get("USER_API_VERSION")}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("USER_SERVICE_PORT", 5202)))
