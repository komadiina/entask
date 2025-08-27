# type: ignore
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from workers import *


def text_recognizer_workflow(workflow_executor: WorkflowExecutor) -> ConductorWorkflow:
    name = "text-recognizer"
    workflow = ConductorWorkflow(name=name, executor=workflow_executor)
    workflow.version = 1

    task_factories: list[Callable[..., object]] = [
        init_easyocr,
        scan_text,
        discard_low_confidence_boxes,
        spellcheck,
        llm_correct,
        init_fpdf2,
        populate_pdf,
        upload_s3,
        forward_url,
    ]

    tasks = [
        fn(text=workflow.input("text"), task_ref_name=f"{fn.__name__}_ref")
        for fn in task_factories
    ]

    for t in tasks:
        workflow >> t

    return workflow
