import asyncio
import os
import json

from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models import StartWorkflowRequest
from conductor.client.orkes_clients import OrkesClients
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from faststream import FastStream
from faststream.nats import NatsBroker

from workflow.workflow import waveformer_workflow
from utils.ws import notify
from models.messages import WSNotification, WorkflowStatus

HOSTS = os.getenv("NATS_HOSTS", "").split(",")
NATS_USER = os.getenv("NATS_USER")
NATS_PASSWORD = os.getenv("NATS_PASSWORD")
NATS_HOST = os.getenv("NATS_HOST")
NATS_CLIENT_PORT = int(os.getenv("NATS_CLIENT_PORT", 4222))
CONDUCTOR_SERVER_HOST = os.getenv("CONDUCTOR_SERVER_HOST")
CONDUCTOR_SERVER_PORT = os.getenv("CONDUCTOR_SERVER_PORT")

CONDUCTOR_SERVER_HOST = "conductor-server"
CONDUCTOR_SERVER_PORT = 8080

CONDUCTOR_SERVER_API_HOST = f"http://{CONDUCTOR_SERVER_HOST}:{CONDUCTOR_SERVER_PORT}"

api_config = Configuration(server_api_url=f"{CONDUCTOR_SERVER_API_HOST}/api")

broker = NatsBroker(
    "nats://{}:{}@{}:{}".format(NATS_USER, NATS_PASSWORD, NATS_HOST, NATS_CLIENT_PORT)
)
app = FastStream(broker)


def register_workflow(
    wf, input, workflow_executor: WorkflowExecutor
) -> ConductorWorkflow:
    workflow = wf(input=input, workflow_executor=workflow_executor)
    workflow.register(overwrite=True)
    return workflow


def init_start_workflow_request(msg_json):
    wf_request = StartWorkflowRequest()
    wf_request.name = "waveformer"
    wf_request.version = 1
    wf_request.input = msg_json
    wf_request.correlation_id = None
    return wf_request


@broker.subscriber(subject="convert.waveformer")
async def handler(msg: str):
    msg_json = json.loads(msg)
    print(msg_json)

    task_handler = TaskHandler(configuration=api_config)
    task_handler.start_processes()

    clients = OrkesClients(api_config)
    wf_executor = clients.get_workflow_executor()
    register_workflow(
        waveformer_workflow, input=msg_json, workflow_executor=wf_executor
    )

    wf_start_request = init_start_workflow_request(msg_json)
    workflow_id = wf_executor.start_workflow(start_workflow_request=wf_start_request)

    notify(
        WSNotification(
            status=WorkflowStatus.STARTED,
            message="Workflow started",
            client_id=msg_json["client_id"],
            data={"workflow_id": workflow_id},
        )
    )


if __name__ == "__main__":
    asyncio.run(app.run())
