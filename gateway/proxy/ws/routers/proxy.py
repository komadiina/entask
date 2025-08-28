import json
from typing import Dict

from fastapi import APIRouter, Request, Response
from models.wsmessages import *
from pydantic import ValidationError
from starlette.websockets import WebSocket, WebSocketDisconnect

websocket_router = APIRouter(prefix="/ws")

# keep track of client ws connections via their tokens
ws_clients: Dict[str, WebSocket] = dict()

# keep track of conversions (conversion_token, client_id), for easier lookup
conversions: Dict[str, str] = dict()


@websocket_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    ws_clients[client_id] = websocket

    try:
        while True:
            data: dict = await websocket.receive_json()

            try:
                ws_msg = WebSocketClientInterrupt.model_validate(data)
            except ValidationError as e:
                continue

            if ws_msg.interrupt_type == InterruptType.PAUSE:
                # TODO: send pause message
                await websocket.send_json({"type": "pause", "client_id": client_id})
            elif ws_msg.interrupt_type == InterruptType.RESUME:
                # TODO: send resume message
                await websocket.send_json({"type": "resume", "client_id": client_id})
            elif ws_msg.interrupt_type == InterruptType.ABORT:
                # TODO: send abort message
                await websocket.send_json({"type": "abort", "client_id": client_id})

    except WebSocketDisconnect:
        del ws_clients[client_id]
    finally:
        await websocket.close()


@websocket_router.post("/proxy/{client_id}")
async def proxy(request: Request, client_id: str):
    if client_id not in ws_clients:
        return Response(
            status_code=404,
            content=json.dumps({"error": "Client not found", "client_id": client_id}),
        )

    try:
        content = await request.json()
        await ws_clients[client_id].send_json(content)
        return {"message": "Message proxied.", "client_id": client_id}
    except Exception as e:
        return Response(
            status_code=500,
            content=json.dumps(
                {
                    "error": "Failed to proxy message.",
                    "client_id": client_id,
                    "error": str(e),
                }
            ),
        )


@websocket_router.get("/clients")
async def get_clients():
    return {"clients": list(ws_clients.keys())}


@websocket_router.post("/proxy-broadcast")
async def proxy_broadcast(request: Request):
    for client in ws_clients.values():
        try:
            json = await request.json()
            await client.send_json(json)
        except Exception as e:
            return Response(
                status_code=500,
                content=json.dumps(
                    {
                        "error": "Failed to proxy message.",
                        "error": str(e),
                    }
                ),
            )
