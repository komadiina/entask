# type: ignore
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from workflow.workers import *


def waveformer_workflow(
    workflow_executor: WorkflowExecutor, input: dict
) -> ConductorWorkflow:
    name = "waveformer"
    workflow = ConductorWorkflow(
        name=name, executor=workflow_executor, description="Waveformer workflow"
    )
    workflow.version = 1
    workflow = workflow.owner_email("test@entask.com")

    t_fetch_raw_document = fetch_raw_document(
        input=input, task_ref_name="fetch_raw_document_ref"
    )
    workflow >> t_fetch_raw_document

    t_init_pedalboard = init_pedalboard(
        input=t_fetch_raw_document.output(), task_ref_name="init_pedalboard_ref"
    )
    workflow >> t_init_pedalboard

    t_apply_effects = apply_effects(
        input=t_init_pedalboard.output(), task_ref_name="apply_effects_ref"
    )
    workflow >> t_apply_effects

    t_upload_s3 = upload_s3(
        input=t_apply_effects.output(), task_ref_name="upload_s3_ref"
    )
    workflow >> t_upload_s3

    t_forward_url = forward_url(
        input=t_upload_s3.output(), task_ref_name="forward_url_ref"
    )
    workflow >> t_forward_url

    return workflow
