import os

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from routers.llm import llm_router

app = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
    docs_url="/api/llm/docs",
    openapi_url="/api/llm/openapi.json",
    redoc_url="/api/llm/redoc",
)

app.include_router(llm_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=int(os.getenv("LLM_SERVICE_PORT", 5207)))
