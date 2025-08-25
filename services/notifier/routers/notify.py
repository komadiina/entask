from fastapi import APIRouter, WebSocket, HTTPException
from fastapi.websockets import WebSocketDisconnect
from typing import Dict

from models.messages import WebSocketMessage

notify_router = APIRouter(prefix="/api/notifier")
ws_clients: Dict[str, WebSocket] = dict()


@notify_router.websocket("/notify/client/{client_id}")
async def notify(websocket: WebSocket, client_id: str):
    await websocket.accept()

    try:
        ws_clients.update({client_id: websocket})
    except Exception as e:
        await websocket.close()
        raise HTTPException(
            status_code=500,
            detail="Failed to register WebSocket client.\n {}".format(str(e)),
        )

    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}, from {client_id}")
        except (WebSocketDisconnect, RuntimeError) as e:
            ws_clients.pop(client_id)
            print(f"WebSocket({client_id}) disconnected.")
            break


@notify_router.post("/notify/client/{client_id}")
async def external_notify(client_id: str, data: WebSocketMessage):
    websocket = ws_clients.get(client_id)

    if websocket is None:
        raise HTTPException(status_code=404, detail="Client not found")

    try:
        await websocket.send_text(f"Message text was: {data}, from {client_id}")
        return {
            "message": "Message sent.",
            "detail": {"client_id": client_id, "data": data},
        }
    except (WebSocketDisconnect, RuntimeError) as e:
        print(f"WebSocket({client_id}) was either disconnected or not open.")
        return HTTPException(status_code=500, detail=str(e))
