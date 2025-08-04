import os
import logging
from fastapi import FastAPI
from models.request import ConversionRequest
from dotenv import load_dotenv

app = FastAPI()
logger = logging.getLogger("videogif-host")
load_dotenv("./dapr.dev.env")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/test")
async def test(input: ConversionRequest):
    print(input.model_dump_json())
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    print(os.environ.get("DAPR_APP_ID_VIDEO_COMPRESSOR"))
    uvicorn.run(app, host="0.0.0.0", port=8000)
