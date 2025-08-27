import json
import os

import httpx
from fastapi import Response
from models.chat import ChatRequest
from models.message import Message, Role

SYSTEM_PROMPT = os.getenv("LLM_SERVICE_SYSTEM_PROMPT", "")
DMR_PROTOCOL = os.getenv("DOCKER_MODEL_RUNNER_PROTOCOL")
DMR_LISTEN = os.getenv("DOCKER_MODEL_RUNNER_LISTEN")
MODEL_NAME = os.getenv("LLM_SERVICE_MODEL", "")


async def send_prompt(req: ChatRequest):
    async with httpx.AsyncClient() as client:
        url = "{}://{}:80/engines/llama.cpp/v1/chat/completions".format(
            DMR_PROTOCOL, DMR_LISTEN
        )

        req_body = ChatRequest(
            model=MODEL_NAME if req.model is None else req.model,
            messages=[Message(role=Role.SYSTEM, content=SYSTEM_PROMPT), *req.messages],
        )

        resp = await client.post(
            url,
            content=req_body.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )

        req_json = resp.json()

        return Response(
            status_code=resp.status_code,
            content=json.dumps(
                {"message": req_json.get("choices")[0].get("message").get("content")}
            ),
        )
