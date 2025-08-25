import os
from fastapi import FastAPI
from routers.notify import notify_router

app = FastAPI(
    docs_url="/api/notifier/docs",
    openapi_url="/api/notifier/openapi.json",
    redoc_url="/api/notifier/redoc",
)

app.include_router(notify_router)


@app.get("/api/notifier/health")
async def health():
    return {"status": "ok"}


@app.get("/api/notifier/version")
async def version():
    return {
        "service": "notifier-service",
        "version": os.environ.get("NOTIFIER_API_VERSION"),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("NOTIFIER_SERVICE_PORT", 5206)))
