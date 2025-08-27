import asyncio
import json
import os

from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from faststream import FastStream
from faststream.nats import NatsBroker
from workflow import text_recognizer_workflow

HOSTS = os.getenv("NATS_HOSTS", "").split(",")
NATS_USER = os.getenv("NATS_USER")
NATS_PASSWORD = os.getenv("NATS_PASSWORD")
NATS_HOST = os.getenv("NATS_HOST")
NATS_CLIENT_PORT = int(os.getenv("NATS_CLIENT_PORT", 4222))

broker = NatsBroker(
    "nats://{}:{}@{}:{}".format(NATS_USER, NATS_PASSWORD, NATS_HOST, NATS_CLIENT_PORT)
)
app = FastStream(broker)

api_config = Configuration(server_api_url="http://conductor-server:8080")
wf_executor = WorkflowExecutor(configuration=api_config)


def register_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    workflow = text_recognizer_workflow(workflow_executor=workflow_executor)
    workflow.register(True)
    return workflow


@broker.subscriber(subject="convert.text-recognizer")
def handler(msg: str):
    print(msg)

    workflow = register_workflow(workflow_executor=wf_executor)
    task_handler = TaskHandler(workflow=workflow)
    task_handler.start_processes()
    wf_run = wf_executor.execute(
        name=workflow.name, version=workflow.version, workflow_input=json.loads(msg)
    )

    print(wf_run.output["result"])
    print(
        "see progress here: {}/execution/{}".format(
            api_config.ui_host, wf_run.workflow_id
        )
    )

    task_handler.stop_processes()


if __name__ == "__main__":
    asyncio.run(app.run())
