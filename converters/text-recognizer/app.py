import asyncio
import json
import os

from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.http.models import StartWorkflowRequest
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from faststream import FastStream
from faststream.nats import NatsBroker
from models.messages import WorkflowStatus, WSNotification
from workflow import text_recognizer_workflow
from ws import notify

HOSTS = os.getenv("NATS_HOSTS", "").split(",")
NATS_USER = os.getenv("NATS_USER")
NATS_PASSWORD = os.getenv("NATS_PASSWORD")
NATS_HOST = os.getenv("NATS_HOST")
NATS_CLIENT_PORT = int(os.getenv("NATS_CLIENT_PORT", 4222))
CONDUCTOR_SERVER_HOST = os.getenv("CONDUCTOR_SERVER_HOST")
CONDUCTOR_SERVER_PORT = os.getenv("CONDUCTOR_UI_SERVER_PORT")

CONDUCTOR_SERVER_HOST = "conductor-server"
CONDUCTOR_SERVER_PORT = 8080

CONDUCTOR_SERVER_API_HOST = f"http://{CONDUCTOR_SERVER_HOST}:{CONDUCTOR_SERVER_PORT}"

api_config = Configuration(server_api_url=f"{CONDUCTOR_SERVER_API_HOST}/api")

broker = NatsBroker(
    "nats://{}:{}@{}:{}".format(NATS_USER, NATS_PASSWORD, NATS_HOST, NATS_CLIENT_PORT)
)
app = FastStream(broker)

# initialize conductor ui via envvars, before Configuration() __init__

wf_executor = WorkflowExecutor(configuration=api_config)
workflow: ConductorWorkflow = None


def register_workflow(
    wf, input, workflow_executor: WorkflowExecutor
) -> ConductorWorkflow:
    workflow = wf(input=input, workflow_executor=workflow_executor)
    workflow.register(overwrite=True)
    return workflow


def init_start_workflow_request(msg_json):
    wf_request = StartWorkflowRequest()
    wf_request.name = "text-recognizer"
    wf_request.version = 1
    wf_request.input = msg_json
    wf_request.correlation_id = None
    return wf_request


@broker.subscriber(subject="convert.text-recognizer")
async def handler(msg: str):
    workflow = register_workflow(
        text_recognizer_workflow, input=json.loads(msg), workflow_executor=wf_executor
    )
    msg_json = json.loads(msg)

    task_handler = TaskHandler(configuration=api_config)
    task_handler.start_processes()

    wf_run = wf_executor.execute(
        name=workflow.name,
        version=workflow.version,
        workflow_input=msg_json,
        request_id=msg_json["token"],
    )


if __name__ == "__main__":
    asyncio.run(app.run())
