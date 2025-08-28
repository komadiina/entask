import os

import httpx

WS_PROXY_HOST = os.getenv("WS_PROXY_HOST")
WS_PROXY_PORT = os.getenv("WS_PROXY_PORT")


def notify(msg: dict):
    print(msg)
    url = f"http://{WS_PROXY_HOST}:{WS_PROXY_PORT}/ws/proxy/{msg.get('user_id')}"

    with httpx.Client() as client:
        client.post(url, json=msg)
