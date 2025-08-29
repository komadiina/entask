import json
import os
import tempfile
import urllib.parse
import uuid

import boto3
import easyocr
import httpx
from conductor.client.worker.worker_task import worker_task
from fpdf import FPDF
from models.messages import WorkflowStatus, WSNotification
from spellchecker import SpellChecker
from utils.ws import notify

S3_HOST = os.getenv("S3_HOST", "minio")
S3_PORT = os.getenv("S3_PORT", 9000)
S3_ENDPOINT = "http://{}:{}".format(S3_HOST, S3_PORT)
S3_BUCKET_CONVERSIONS = os.getenv("S3_BUCKET_CONVERSIONS", "conversions")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
URI_TTL = 300


@worker_task(task_definition_name="tr-fetch-raw-document")
def fetch_raw_document(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Fetching raw document...",
            client_id=input["client_id"],
        )
    )

    with httpx.Client() as client:
        FILE_SERVICE_HOST = os.getenv("FILE_SERVICE_HOST", "file-service")
        FILE_SERVICE_PORT = os.getenv("FILE_SERVICE_PORT", 5204)
        url = "http://{}:{}/api/file/presign/download/raw".format(
            FILE_SERVICE_HOST, FILE_SERVICE_PORT
        )
        response = client.post(
            url, content=json.dumps({"object_key": input["object_key"]})
        )

        if response.status_code != 200:
            raise Exception("Failed to fetch raw document")

        download_url = response.json()["url"]

        response = client.get(
            download_url, headers={"Accept": "application/octet-stream"}
        )

        document_content = response.content

    tmp = tempfile.NamedTemporaryFile(prefix="rawdoc-", delete=False)
    tmp.write(document_content)
    tmp.flush()
    tmp.close()
    path = tmp.name

    return {
        **input,
        "file_path": path,
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

    return {**input}


@worker_task(task_definition_name="tr-scan-input")
def scan_text(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Scanning input with EasyOCR...",
            client_id=input["client_id"],
        )
    )

    with open(input["file_path"], "rb") as f:
        img = f.read()

    reader = easyocr.Reader(
        ["en"],
        gpu=True,
        download_enabled=False,
        model_storage_directory="/.EasyOCR/model",
    )
    result = reader.readtext(img, detail=1)

    return {**input, "result": result}


@worker_task(task_definition_name="tr-discard-low-confidence-boxes")
def discard_low_confidence_boxes(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Discarding low confidence boxes...",
            client_id=input["client_id"],
        )
    )

    input["result"] = [bbox for bbox in input["result"] if bbox[2] > 0.25]

    # flatten list
    input["result"] = [sublist[1] for sublist in input["result"]]

    return {**input}


@worker_task(task_definition_name="tr-spellcheck")
def spellcheck(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Spellchecking text with pyspellcheck...",
            client_id=input["client_id"],
        )
    )

    spell = SpellChecker()

    def decisive_spellcheck(word: str) -> str:
        corrected = spell.correction(word)
        if corrected:
            return corrected
        else:
            return word

    result = []
    for word in input["result"]:
        if word.count(" "):
            # split into words, spellcheck each word, join back
            result.append(" ".join([decisive_spellcheck(w) for w in word.split(" ")]))
        else:
            result.append(decisive_spellcheck(word))

    input["result"] = result

    return {
        **input,
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

    try:
        with httpx.Client() as client:
            LLM_SERVICE_HOST = os.getenv("LLM_SERVICE_HOST", "llm-service")
            LLM_SERVICE_PORT = os.getenv("LLM_SERVICE_PORT", 5207)
            url = "http://{}:{}/api/llm/chat".format(LLM_SERVICE_HOST, LLM_SERVICE_PORT)

            response = client.post(
                url,
                json={"messages": [" ".join(input["result"])]},
            )

            if response.status_code != 200:
                raise Exception("Failed to correct text artifacts.")

            input["result"] = (response.json())["message"]
    except:
        input["result"] = " ".join(input["result"])

    return {
        **input,
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

    pdf_doc = {
        "name": input["client_id"] + ".pdf",
        "font": "helvetica",
        "font_size": 12,
    }

    return {**input, "pdf_doc": pdf_doc}


@worker_task(task_definition_name="tr-populate-pdf")
def populate_pdf(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Populating PDF...",
            client_id=input["client_id"],
        )
    )

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font(input["pdf_doc"]["font"], "", input["pdf_doc"]["font_size"])
    pdf.multi_cell(w=150, h=10, text=input["result"])
    pdf.output("/tmp/" + input["pdf_doc"]["name"])

    return {
        **input,
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

    with httpx.Client() as client:
        object_key = (
            f"{input['client_id']}-{input['pdf_doc']['name']}-{uuid.uuid4()}.pdf"
        )
        s3_client = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
        )

        s3_client.upload_file(
            Filename="/tmp/" + input["pdf_doc"]["name"],
            Bucket=S3_BUCKET_CONVERSIONS,
            Key=object_key,
        )

        input["downloadUri"] = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": S3_BUCKET_CONVERSIONS,
                "Key": object_key,
            },
            ExpiresIn=URI_TTL,
        ).replace(S3_HOST, "localhost")

    return {
        **input,
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
            data={"downloadUri": input["downloadUri"]},
        )
    )

    # cleanup
    os.remove("/tmp/" + input["pdf_doc"]["name"])

    return {
        **input,
    }
