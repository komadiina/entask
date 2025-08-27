import asyncio
import json
import os

from faststream import FastStream
from faststream.nats import NatsBroker

HOSTS = ["nats-1", "nats-2", "nats-3"]
NATS_USER = os.getenv("NATS_USER")
NATS_PASSWORD = os.getenv("NATS_PASSWORD")
NATS_HOST = os.getenv("NATS_HOST")
NATS_CLIENT_PORT = int(os.getenv("NATS_CLIENT_PORT", 4222))

WS_PROXY_HOST = os.getenv("WS_PROXY_HOST")
WS_PROXY_PORT = os.getenv("WS_PROXY_PORT")

broker = NatsBroker(
    "nats://{}:{}@{}:{}".format(NATS_USER, NATS_PASSWORD, NATS_HOST, NATS_CLIENT_PORT)
)
app = FastStream(broker)


@broker.subscriber(subject="convert.thumbnailer")
async def handler(msg: str):
    print(msg)
    print(json.loads(msg))


if __name__ == "__main__":
    asyncio.run(app.run())
