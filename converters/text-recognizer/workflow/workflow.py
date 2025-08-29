# type: ignore
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from workflow.workers import *


def text_recognizer_workflow(
    workflow_executor: WorkflowExecutor, input: dict
) -> ConductorWorkflow:
    name = "text-recognizer"
    workflow = ConductorWorkflow(
        name=name, executor=workflow_executor, description="Text recognition workflow"
    )
    workflow.version = 1
    workflow = workflow.owner_email("test@entask.com")

    t_fetch_raw_document = fetch_raw_document(
        input=input, task_ref_name="fetch_raw_document_ref"
    )
    workflow >> t_fetch_raw_document

    t_init_easyocr = init_easyocr(
        input=t_fetch_raw_document.output(), task_ref_name="init_easyocr_ref"
    )
    workflow >> t_init_easyocr

    t_scan_text = scan_text(
        input=t_init_easyocr.output(), task_ref_name="scan_text_ref"
    )
    workflow >> t_scan_text

    t_discard_low_confidence_boxes = discard_low_confidence_boxes(
        input=t_scan_text.output(), task_ref_name="discard_low_confidence_boxes_ref"
    )
    workflow >> t_discard_low_confidence_boxes

    t_spellcheck = spellcheck(
        input=t_discard_low_confidence_boxes.output(), task_ref_name="spellcheck_ref"
    )
    workflow >> t_spellcheck

    t_llm_correct = llm_correct(
        input=t_spellcheck.output(), task_ref_name="llm_correct_ref"
    )
    workflow >> t_llm_correct

    t_init_fpdf2 = init_fpdf2(
        input=t_llm_correct.output(), task_ref_name="init_fpdf2_ref"
    )
    workflow >> t_init_fpdf2

    t_populate_pdf = populate_pdf(
        input=t_init_fpdf2.output(), task_ref_name="populate_pdf_ref"
    )
    workflow >> t_populate_pdf

    t_upload_s3 = upload_s3(
        input=t_populate_pdf.output(), task_ref_name="upload_s3_ref"
    )
    workflow >> t_upload_s3

    t_forward_url = forward_url(
        input=t_upload_s3.output(), task_ref_name="forward_url_ref"
    )
    workflow >> t_forward_url

    return workflow
