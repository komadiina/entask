import os
import uuid

from faststream.nats import JStream, NatsBroker
from faststream.nats.fastapi import NatsRouter
from models.conversion import ConversionRequest

NATS_USER = os.getenv("NATS_USER")
NATS_PASSWORD = os.getenv("NATS_PASSWORD")
NATS_HOST = os.getenv("NATS_HOST")
NATS_CLIENT_PORT = int(os.getenv("NATS_CLIENT_PORT", 4222))
NATS_CONNINFO = (
    "nats://{}:{}@{}:{}".format(NATS_USER, NATS_PASSWORD, NATS_HOST, NATS_CLIENT_PORT),
)

convert_router = NatsRouter(
    NATS_CONNINFO,
    prefix="/api/conversion",
)

broker = NatsBroker(NATS_CONNINFO)


@convert_router.post("/submit")
async def submit_conversion(conversion: ConversionRequest):
    await broker.connect()
    await broker.start()

    conversion.token = uuid.uuid4().hex

    await broker.publisher(subject="convert.{}".format(conversion.type)).publish(
        conversion.model_dump_json()
    )

    return {
        "message": "Conversion request published.",
        "subject": "convert.{}".format(conversion.type),
        "conversion": conversion,
    }
