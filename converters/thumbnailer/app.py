from faststream import FastStream
from faststream.nats import NatsBroker
import os
import asyncio

HOSTS = ["nats-1", "nats-2", "nats-3"]
NATS_USER = os.getenv("NATS_USER")
NATS_PASSWORD = os.getenv("NATS_PASSWORD")
NATS_HOST = os.getenv("NATS_HOST")
NATS_CLIENT_PORT = int(os.getenv("NATS_CLIENT_PORT", 4222))

broker = NatsBroker(
    "nats://{}:{}@{}:{}".format(NATS_USER, NATS_PASSWORD, NATS_HOST, NATS_CLIENT_PORT)
)
app = FastStream(broker)


@broker.subscriber(subject="convert.thumbnailer")
async def handler(msg: str):
    # TODO
    print(msg)


if __name__ == "__main__":
    asyncio.run(app.run())
