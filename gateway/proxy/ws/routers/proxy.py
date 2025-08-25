import json
from typing import Dict

from fastapi import APIRouter, Response
from models.wsmessages import *
from pydantic import ValidationError
from starlette.websockets import WebSocket, WebSocketDisconnect

ws_clients: Dict[str, WebSocket] = dict()
websocket_router = APIRouter(prefix="/ws")


@websocket_router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    ws_clients[client_id] = websocket

    try:
        while True:
            data: dict = await websocket.receive_json()

            try:
                msg = WebSocketClientInterrupt.model_validate(data)
            except ValidationError as exc:
                await websocket.send_json(
                    WebSocketServerMessage(data=exc.errors()).model_dump_json()
                )
                continue

            if msg.type == WSMessageType.WorkflowInterrupt:
                await websocket.send_json(
                    WebSocketInterruptResponse(
                        status=AckStatus.Ack, error=None
                    ).model_dump_json()
                )
            elif msg.type == WSMessageType.Other:
                await websocket.send_json(
                    WebSocketServerMessage(
                        data={"message": "Received other message."}
                    ).model_dump_json()
                )

    except WebSocketDisconnect:
        del ws_clients[client_id]
    finally:
        await websocket.close()


@websocket_router.post("/proxy/{client_id}")
async def proxy(client_id: str, data: TWSServerMessage):
    if client_id not in ws_clients:
        return Response(
            status_code=404,
            content=json.dumps({"error": "Client not found", "client_id": client_id}),
        )

    try:
        await ws_clients[client_id].send_json(data.model_dump_json())
        return {"message": "Message proxied.", "client_id": client_id}
    except:
        return Response(
            status_code=500,
            content=json.dumps(
                {"error": "Failed to proxy message.", "client_id": client_id}
            ),
        )


@websocket_router.get("/clients")
async def get_clients():
    return {"clients": list(ws_clients.keys())}
