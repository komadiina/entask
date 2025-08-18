import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from models.request import ConversionRequest

app = FastAPI()
logger = logging.getLogger("videogif-host")
load_dotenv("./dapr.dev.env")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/test")
async def test(input: ConversionRequest):
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
