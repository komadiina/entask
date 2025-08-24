from conversion.app import app
from fastapi import APIRouter, Request
from models.conversion import ConversionRequest
from nats.aio.client import Client as NATSClient

convert_router = APIRouter(prefix="/api/convert")


@convert_router.post("/submit")
async def submit_conversion(request: Request, conversion: ConversionRequest):
    # 1. fetch nats client from app state
    nats_client: NATSClient = app.state.nats_client

    # 2. init jetstream
    jetstream = nats_client.jetstream()

    # 3. persist messages on appropriate conversion subject
    subject = "convert.{}".format(conversion.type)
    ack = await jetstream.publish(subject, conversion.object_key.encode("utf-8"))
    print(ack)

    await nats_client.close()

    print(request.body)
    return {"ok": "helo wordl"}
