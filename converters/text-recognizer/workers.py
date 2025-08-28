import time

from conductor.client.worker.worker_task import worker_task
from ws import notify


@worker_task(task_definition_name="tr-init-easyocr")
def init_easyocr(input: dict):
    time.sleep(5)
    notify(
        {
            **input,
            "message": "easy-ocr initialized",
            "status": "ok",
        }
    )
    return {
        **input,
        "message": "easy-ocr initialized",
    }


@worker_task(task_definition_name="tr-scan-input")
def scan_text(input: dict):

    notify(
        {
            **input,
            "message": "input scanned",
            "status": "ok",
        }
    )
    return {
        **input,
        "message": "input scanned",
    }


@worker_task(task_definition_name="tr-discard-low-confidence-boxes")
def discard_low_confidence_boxes(input: dict):

    notify(
        {
            **input,
            "message": "low confidence boxes discarded",
            "status": "ok",
        }
    )
    return {
        **input,
        "message": "low confidence boxes discarded",
    }


@worker_task(task_definition_name="tr-spellcheck")
def spellcheck(input: dict):

    notify(
        {
            "user_id": input["user_id"],
            "message": "input: dict spellchecked",
        }
    )
    return {
        **input,
        "message": "input: dict spellchecked",
    }


@worker_task(task_definition_name="tr-llm-correct")
def llm_correct(input: dict):

    notify(
        {
            **input,
            "message": "input: dict llm-corrected",
            "status": "ok",
        }
    )
    return {
        **input,
        "message": "input: dict llm-corrected",
    }


@worker_task(task_definition_name="tr-init-fpdf2")
def init_fpdf2(input: dict):

    notify(
        {
            **input,
            "message": "fpdf2 initialized",
            "status": "ok",
        }
    )
    return {
        **input,
        "message": "fpdf2 initialized",
    }


@worker_task(task_definition_name="tr-populate-pdf")
def populate_pdf(input: dict):

    notify(
        {
            **input,
            "message": "pdf populated",
            "status": "ok",
        }
    )
    return {
        **input,
        "message": "pdf populated",
    }


@worker_task(task_definition_name="tr-upload-s3")
def upload_s3(input: dict):

    notify(
        {
            **input,
            "message": "s3 uploaded",
            "status": "ok",
        }
    )
    return {
        **input,
        "message": "s3 uploaded",
    }


@worker_task(task_definition_name="tr-client-forward-url")
def forward_url(input: dict):

    notify(
        {
            **input,
            "message": "url forwarded to client",
            "status": "ok",
        }
    )
    return {
        **input,
        "message": "url forwarded to client",
    }
