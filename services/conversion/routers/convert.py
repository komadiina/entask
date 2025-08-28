import os
import uuid

from conductor.client.configuration.configuration import Configuration
from conductor.client.orkes_clients import OrkesClients
from fastapi import HTTPException, Request
from faststream.nats import NatsBroker
from faststream.nats.fastapi import NatsRouter
from models.conversion import ConversionRequest
from models.messages import WorkflowStatus, WSNotification
from utils.ws import notify

NATS_USER = os.getenv("NATS_USER")
NATS_PASSWORD = os.getenv("NATS_PASSWORD")
NATS_HOST = os.getenv("NATS_HOST")
NATS_CLIENT_PORT = int(os.getenv("NATS_CLIENT_PORT", 4222))
NATS_CONNINFO = (
    "nats://{}:{}@{}:{}".format(NATS_USER, NATS_PASSWORD, NATS_HOST, NATS_CLIENT_PORT),
)
CONDUCTOR_SERVER_HOST = os.getenv("CONDUCTOR_SERVER_HOST")
CONDUCTOR_SERVER_PORT = os.getenv("CONDUCTOR_SERVER_PORT")
CONDUCTOR_SERVER_API_HOST = (
    f"http://{CONDUCTOR_SERVER_HOST}:{CONDUCTOR_SERVER_PORT}/api"
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


@convert_router.delete("/{workflow_id}")
async def abort_workflow(workflow_id: str, request: Request):
    try:
        client_id = (await request.json())["clientId"]

        config = Configuration(server_api_url=CONDUCTOR_SERVER_API_HOST)
        clients = OrkesClients(config)
        wf_client = clients.get_workflow_client()
        wf_client.terminate_workflow(workflow_id)

        notify(
            WSNotification(
                status=WorkflowStatus.ABORTED,
                message="Workflow aborted.",
                client_id=client_id,
                data={"workflow_id": workflow_id},
            )
        )
        return {"message": "Workflow aborted."}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to abort workflow.")


@convert_router.put("/{workflow_id}/pause")
async def pause_workflow(workflow_id: str, request: Request):
    try:
        client_id = (await request.json())["clientId"]

        config = Configuration(server_api_url=CONDUCTOR_SERVER_API_HOST)
        clients = OrkesClients(config)
        wf_client = clients.get_workflow_client()
        wf_client.terminate_workflow(workflow_id)

        notify(
            WSNotification(
                status=WorkflowStatus.PAUSED,
                message="Workflow paused.",
                client_id=client_id,
                data={"workflow_id": workflow_id},
            )
        )
        return {"message": "Workflow paused."}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to pause workflow.")


@convert_router.put("/{workflow_id}/resume")
async def resume_workflow(workflow_id: str, request: Request):
    try:
        client_id = (await request.json())["clientId"]

        config = Configuration(server_api_url=CONDUCTOR_SERVER_API_HOST)
        clients = OrkesClients(config)
        wf_client = clients.get_workflow_client()
        wf_client.terminate_workflow(workflow_id)

        notify(
            WSNotification(
                status=WorkflowStatus.RESUMED,
                message="Workflow resumed.",
                client_id=client_id,
                data={"workflow_id": workflow_id},
            )
        )
        return {
            "message": "Workflow resumed.",
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to resume workflow.")
