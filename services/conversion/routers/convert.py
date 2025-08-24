from fastapi import APIRouter, HTTPException, Request
from models.conversion import ConversionRequest
from nats.aio.client import Client as NATSClient

convert_router = APIRouter(prefix="/api/conversion")


@convert_router.post("/submit")
async def submit_conversion(request: Request, conversion: ConversionRequest):
    if not request.app.state.nats_client.is_connected:
        raise HTTPException(detail="NATS connection is not open", status_code=503)

    # 1. fetch nats client from app state
    nats_client: NATSClient = request.app.state.nats_client

    # 2. init jetstream
    jetstream = nats_client.jetstream()

    # 3. persist messages on appropriate conversion subject
    subject = "convert.{}".format(conversion.type)
    ack = await jetstream.publish(subject, conversion.object_key.encode("utf-8"))
    return {"ack": ack}
