from typing import Any, Dict, Optional, Union

from models.camelizer import BaseSchema

# /services/notifier/routers/notify.py
# service receives: {data: any}, client_id from pathparam on http:// POST
# service sends: {message: string, client_id: string, status: string | enum, data: any} on ws://../notify/client

# service receives {signal: str | enum, conversion_token: str}, client_id from pathparam, on ws://../conversion/ws ->
#   -> forwards the ws message to dapr
# service sends: {message: string, client_id: string, status: string | enum, data: any} on ws://../conversions/ws


class WebSocketMessage(BaseSchema):
    client_id: str
    status: str
    message: str
    data: Optional[Union[Dict[str, Any], str]] = None


class WSSentMessage(WebSocketMessage):
    client_id: str
    status: str


class WSReceivedMessage(WebSocketMessage):
    client_id: str
