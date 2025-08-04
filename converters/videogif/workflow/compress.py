from dapr.ext.workflow import WorkflowActivityContext, WorkflowRuntime
from dapr.clients import DaprClient
from models.request import ConversionRequest
from models.workflow import CompressionWorkflowOutput

import time


def main(
    ctx: WorkflowActivityContext, input: ConversionRequest
) -> CompressionWorkflowOutput:
    print("Compressing thumbnails...")
    time.sleep(1)

    return CompressionWorkflowOutput(
        data=input,
        processing=True,
        finished=False,
        status="thumbnails_compressed",
    )
