from models.conversion import ConversionRequest
from faststream.nats import JStream, NatsBroker
from faststream.nats.fastapi import NatsRouter

import os

NATS_USER = os.getenv("NATS_USER")
NATS_PASSWORD = os.getenv("NATS_PASSWORD")
NATS_HOST = os.getenv("NATS_HOST")
NATS_CLIENT_PORT = int(os.getenv("NATS_CLIENT_PORT", 4222))

convert_router = NatsRouter(
    "nats://{}:{}@{}:{}".format(NATS_USER, NATS_PASSWORD, NATS_HOST, NATS_CLIENT_PORT),
    prefix="/api/conversion",
)
broker = NatsBroker("nats://nats:nats@nats-1:4222")


@convert_router.post("/submit")
async def submit_conversion(conversion: ConversionRequest):
    await broker.connect()
    await broker.start()

    await broker.publisher(subject="convert.thumbnailer").publish(conversion.object_key)
    return {"message": "Conversion request published."}
