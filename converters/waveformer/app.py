import asyncio
import os

from faststream import FastStream
from faststream.nats import NatsBroker

HOSTS = os.getenv("NATS_HOSTS", "").split(",")
NATS_USER = os.getenv("NATS_USER")
NATS_PASSWORD = os.getenv("NATS_PASSWORD")
NATS_HOST = os.getenv("NATS_HOST")
NATS_CLIENT_PORT = int(os.getenv("NATS_CLIENT_PORT", 4222))

broker = NatsBroker(
    "nats://{}:{}@{}:{}".format(NATS_USER, NATS_PASSWORD, NATS_HOST, NATS_CLIENT_PORT)
)
app = FastStream(broker)


@broker.subscriber(subject="convert.waveformer")
async def handler(msg: str):
    # TODO
    pass


if __name__ == "__main__":
    asyncio.run(app.run())
