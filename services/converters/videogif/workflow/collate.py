import time

from dapr.clients import DaprClient
from dapr.ext.workflow import WorkflowActivityContext, WorkflowRuntime
from models.request import ConversionRequest


def main(ctx: WorkflowActivityContext, data: ConversionRequest):
    print("Collating thumbnails into a GIF...")
    time.sleep(1)

    return {
        "data": data,
        "processing": False,
        "finished": True,
        "status": "thumbnails_collated",
    }
