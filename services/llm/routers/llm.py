import os

from fastapi import APIRouter, HTTPException, Request
from functions.chat import send_prompt
from models.chat import ChatRequest

llm_router = APIRouter(prefix="/api/llm")


@llm_router.post("/chat")
async def chat(request: Request, chat_request: ChatRequest):
    try:
        response = await send_prompt(chat_request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@llm_router.get("/model")
async def get_model():
    return {"model": os.getenv("LLM_SERVICE_MODEL", "")}
