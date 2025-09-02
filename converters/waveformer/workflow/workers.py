# type: ignore
import json
import os
import tempfile
import uuid

import boto3
import httpx
from conductor.client.worker.worker_task import worker_task
from models.messages import WorkflowStatus, WSNotification
from pedalboard import Chorus, Compressor, Gain, Pedalboard, Reverb
from pedalboard.io import AudioFile
from utils.ws import notify

S3_HOST = os.getenv("S3_HOST", "minio")
S3_PORT = os.getenv("S3_PORT", 9000)
S3_ENDPOINT = "http://{}:{}".format(S3_HOST, S3_PORT)
S3_BUCKET_CONVERSIONS = os.getenv("S3_BUCKET_CONVERSIONS", "conversions")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
URI_TTL = 300


@worker_task(task_definition_name="wavf-fetch-raw-document")
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


@worker_task(task_definition_name="wavf-init-pedalboard")
def init_pedalboard(input: dict):
    pb_doc = {"name": input["client_id"] + ".wav"}

    return {**input, "pb_doc": pb_doc}


@worker_task(task_definition_name="wavf-apply-effects")
def apply_effects(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Applying effects...",
            client_id=input["client_id"],
        )
    )

    with AudioFile(input["file_path"]) as f:
        audio = f.read(f.frames)

    effects = []
    for effect in input["additional"]:
        if effect["label"].lower() == "chorus":
            depth = effect["depth"]
            rate = effect["rate"]
            mix = effect["mix"]
            effects.append(Chorus(depth=depth, rate_hz=rate))
        elif effect["label"].lower() == "compression":
            attack = effect["attack"]
            release = effect["release"]
            threshold = effect["threshold"]
            mix = effect["mix"]
            effects.append(
                Compressor(
                    attack_ms=attack,
                    release_ms=release,
                    threshold_db=threshold,
                )
            )
        elif effect["label"].lower() == "gain":
            gain = effect["gain"]
            effects.append(Gain(gain_db=gain))
        elif effect["label"].lower() == "reverb":
            room_size = effect["roomSize"]
            wet = effect["wet"]
            dry = effect["dry"]
            mix = effect["mix"]
            effects.append(
                Reverb(
                    room_size=room_size if room_size <= 1 else 1,
                    dry_level=dry,
                    wet_level=wet,
                )
            )

    board = Pedalboard(effects)
    mixed = board(audio, 44100.0)

    with AudioFile(
        "/tmp/" + input["pb_doc"]["name"], "w", samplerate=44100, num_channels=2
    ) as f:
        f.write(mixed)

    return {**input}


@worker_task(task_definition_name="wavf-upload-s3")
def upload_s3(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Uploading WAV to S3...",
            client_id=input["client_id"],
        )
    )

    with httpx.Client() as client:
        object_key = (
            f"{input['client_id']}-{input['pb_doc']['name']}-{uuid.uuid4()}.wav"
        )
        s3_client = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
        )

        s3_client.upload_file(
            Filename="/tmp/" + input["pb_doc"]["name"],
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


@worker_task(task_definition_name="wavf-forward-url")
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
    os.remove("/tmp/" + input["pb_doc"]["name"])
    os.remove(input["file_path"])

    return {
        **input,
    }
