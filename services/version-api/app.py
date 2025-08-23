import os

import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],  # xd
            allow_methods=["*"],
            allow_headers=["*"],  # xd
        )
    ]
)


@app.get("/api/version")
async def version(response: Response):
    response.status_code = 200
    return {"service": "version-service", "version": "v1"}


@app.get("/api/version/health", status_code=200)
async def health():
    return {"status": "ok"}


@app.get("/api/version/auth")
async def auth(request: Request):
    AUTH_HOST = os.getenv("AUTH_API_HOST", "auth-service")
    AUTH_PORT = os.getenv("AUTH_SERVICE_PORT", 5201)

    url = f"http://{AUTH_HOST}:{AUTH_PORT}/api/auth/version"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"connect error: {e}")

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@app.get("/api/version/user-details")
async def user_details(request: Request):
    USER_DETAILS_API_HOST = os.getenv("AUTH_API_HOST", "auth-service")
    USER_DETAILS_SERVICE_PORT = os.getenv("AUTH_SERVICE_PORT", 5201)

    url = f"http://{USER_DETAILS_API_HOST}:{USER_DETAILS_SERVICE_PORT}/api/user-details/version"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"connect error: {e}")

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@app.get("/api/version/file")
async def file(request: Request):
    FILE_API_HOST = os.getenv("FILE_API_HOST", "file-service")
    FILE_SERVICE_PORT = os.getenv("FILE_SERVICE_PORT", 5202)

    url = f"http://{FILE_API_HOST}:{FILE_SERVICE_PORT}/api/file/version"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"connect error: {e}")

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("VERSION_SERVICE_PORT", 5200)))
