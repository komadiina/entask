import time

from conductor.client.worker.worker_task import worker_task


@worker_task(task_definition_name="tr-init-easyocr")
def init_easyocr(text):
    time.sleep(1)
    return "easy-ocr initialized"


@worker_task(task_definition_name="tr-scan-text")
def scan_text(text):
    time.sleep(1)
    return "text scanned"


@worker_task(task_definition_name="tr-discard-low-confidence-boxes")
def discard_low_confidence_boxes(text):
    time.sleep(1)
    return "low confidence boxes discarded"


@worker_task(task_definition_name="tr-spellcheck")
def spellcheck(text):
    time.sleep(1)
    return "text spellchecked"


@worker_task(task_definition_name="tr-llm-correct")
def llm_correct(text):
    time.sleep(1)
    return "text llm-corrected"


@worker_task(task_definition_name="tr-init-fpdf2")
def init_fpdf2(text):
    time.sleep(1)
    return "fpdf2 initialized"


@worker_task(task_definition_name="tr-populate-pdf")
def populate_pdf(text):
    time.sleep(1)
    return "pdf populated"


@worker_task(task_definition_name="tr-upload-s3")
def upload_s3(text):
    time.sleep(1)
    return "s3 uploaded"


@worker_task(task_definition_name="tr-client-forward-url")
def forward_url(text):
    time.sleep(1)
    return "url forwarded to client"
