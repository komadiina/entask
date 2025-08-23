import os

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from routers.file import file_router

app = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]
)
app.include_router(file_router)


@app.get("/api/file/version")
async def version():
    return {
        "service": "file-service",
        "version": os.getenv("FILE_API_VERSION", "v1"),
    }


@app.get("/api/file/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("FILE_SERVICE_PORT", 5203)))
