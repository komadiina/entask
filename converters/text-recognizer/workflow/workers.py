import time

from conductor.client.worker.worker_task import worker_task
from models.messages import WorkflowStatus, WSNotification
from utils.ws import notify


@worker_task(task_definition_name="tr-fetch-raw-document")
def fetch_raw_document(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Fetching raw document...",
            client_id=input["client_id"],
        )
    )

    time.sleep(2)

    return {
        **input,
        "message": "raw document fetched",
    }


@worker_task(task_definition_name="tr-init-easyocr")
def init_easyocr(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Initializing EasyOCR...",
            client_id=input["client_id"],
        )
    )

    time.sleep(2)

    return {
        **input,
        "message": "easy-ocr initialized",
    }


@worker_task(task_definition_name="tr-scan-input")
def scan_text(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Scanning input with EasyOCR...",
            client_id=input["client_id"],
        )
    )

    time.sleep(2)

    return {
        **input,
        "message": "input scanned",
    }


@worker_task(task_definition_name="tr-discard-low-confidence-boxes")
def discard_low_confidence_boxes(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Discarding low confidence boxes...",
            client_id=input["client_id"],
        )
    )
    return {
        **input,
        "message": "low confidence boxes discarded",
    }


@worker_task(task_definition_name="tr-spellcheck")
def spellcheck(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Spellchecking text with pyspellcheck...",
            client_id=input["client_id"],
        )
    )

    return {
        **input,
        "message": "input: dict spellchecked",
    }


@worker_task(task_definition_name="tr-llm-correct")
def llm_correct(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Correcting text artifacts using local LLM...",
            client_id=input["client_id"],
        )
    )

    time.sleep(4)

    return {
        **input,
        "message": "input: dict llm-corrected",
    }


@worker_task(task_definition_name="tr-init-fpdf2")
def init_fpdf2(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Initializing PDF (fpdf2) document...",
            client_id=input["client_id"],
        )
    )
    return {
        **input,
        "message": "fpdf2 initialized",
    }


@worker_task(task_definition_name="tr-populate-pdf")
def populate_pdf(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Populating PDF...",
            client_id=input["client_id"],
        )
    )
    return {
        **input,
        "message": "pdf populated",
    }


@worker_task(task_definition_name="tr-upload-s3")
def upload_s3(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Uploading PDF to S3...",
            client_id=input["client_id"],
        )
    )

    time.sleep(2)

    return {
        **input,
        "message": "s3 uploaded",
    }


@worker_task(task_definition_name="tr-client-forward-url")
def forward_url(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Forwarding S3 URL to client...",
            client_id=input["client_id"],
        )
    )

    notify(
        WSNotification(
            status=WorkflowStatus.SUCCEEDED,
            message="Conversion finished!",
            client_id=input["client_id"],
            data={"downloadUri": "https://google.com"},
        )
    )

    return {
        **input,
        "message": "url forwarded to client",
        "downloadUri": "https://google.com",
    }
