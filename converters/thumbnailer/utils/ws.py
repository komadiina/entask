import os

import httpx
from models.messages import WSNotification

WS_PROXY_HOST = os.getenv("WS_PROXY_HOST")
WS_PROXY_PORT = os.getenv("WS_PROXY_PORT")


def notify(msg: WSNotification):
    url = f"http://{WS_PROXY_HOST}:{WS_PROXY_PORT}/ws/proxy/{msg.client_id}"

    with httpx.Client() as client:
        client.post(url, json=msg.model_dump_json())
