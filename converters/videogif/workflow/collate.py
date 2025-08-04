from dapr.ext.workflow import WorkflowActivityContext, WorkflowRuntime
from dapr.clients import DaprClient
from models.request import ConversionRequest

import time


def main(ctx: WorkflowActivityContext, data: ConversionRequest):
    print("Collating thumbnails into a GIF...")
    time.sleep(1)

    return {
        "data": data,
        "processing": False,
        "finished": True,
        "status": "thumbnails_collated",
    }
