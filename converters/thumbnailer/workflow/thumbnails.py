import time

from dapr.clients import DaprClient
from dapr.ext.workflow import WorkflowActivityContext, WorkflowRuntime
from models.request import ConversionRequest


def main(ctx: WorkflowActivityContext, data: ConversionRequest):
    print("Extracting thumbnails")
    time.sleep(1)

    return {
        "data": data,
        "processing": True,
        "finished": False,
        "status": "extracted_thumbnails",
    }
