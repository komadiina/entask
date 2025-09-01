# type: ignore
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from workflow.workers import *


def thumbnailer_workflow(
    workflow_executor: WorkflowExecutor, input: dict
) -> ConductorWorkflow:
    name = "thumbnailer"
    workflow = ConductorWorkflow(
        name=name, executor=workflow_executor, description="Thumbnailer workflow"
    )
    workflow.version = 1
    workflow = workflow.owner_email("test@entask.com")

    t_fetch_raw_document = fetch_raw_document(
        input=input, task_ref_name="fetch_raw_document_ref"
    )
    workflow >> t_fetch_raw_document

    t_downscale_clamp = downscale_clamp(
        input=t_fetch_raw_document.output(), task_ref_name="downscale_clamp_ref"
    )
    workflow >> t_downscale_clamp

    t_sample_video = sample_video(
        input=t_downscale_clamp.output(), task_ref_name="sample_video_ref"
    )
    workflow >> t_sample_video

    t_save_to_gif = save_to_gif(
        input=t_sample_video.output(), task_ref_name="save_to_gif_ref"
    )
    workflow >> t_save_to_gif

    t_zip_contents = zip_contents(
        input=t_save_to_gif.output(), task_ref_name="zip_contents_ref"
    )
    workflow >> t_zip_contents

    t_upload_s3 = upload_s3(
        input=t_zip_contents.output(), task_ref_name="upload_s3_ref"
    )
    workflow >> t_upload_s3

    t_forward_url = forward_url(
        input=t_upload_s3.output(), task_ref_name="forward_url_ref"
    )
    workflow >> t_forward_url

    return workflow
