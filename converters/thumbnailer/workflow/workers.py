# type: ignore
import json
import math
import os
import tempfile
import uuid
from zipfile import ZipFile

import boto3
import httpx
import imageio
from conductor.client.worker.worker_task import worker_task
from models.messages import WorkflowStatus, WSNotification
from moviepy import VideoFileClip
from utils.ws import notify

S3_HOST = os.getenv("S3_HOST", "minio")
S3_PORT = os.getenv("S3_PORT", 9000)
S3_ENDPOINT = "http://{}:{}".format(S3_HOST, S3_PORT)
S3_BUCKET_CONVERSIONS = os.getenv("S3_BUCKET_CONVERSIONS", "conversions")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
URI_TTL = 300
MAX_PIXELS = 2_000_000
MAX_W = 1280
MAX_H = 720
FRAME_COUNT = 10
TMP_DIR = "/tmp"
JPEG_PREFIX = "tbnlr_frame_"
GIF_FILENAME = "tbnlr_preview.gif"


@worker_task(task_definition_name="tbnlr-fetch-raw-document")
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


@worker_task(task_definition_name="tbnlr-downscale-clamp")
def downscale_clamp(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Downscaling video...",
            client_id=input["client_id"],
        )
    )

    clip = VideoFileClip(input["file_path"])
    try:
        w, h = int(clip.w), int(clip.h)
        pixels = w * h

        # compute factor that satisfies both pixel and dimension caps
        factor_pixels = math.sqrt(MAX_PIXELS / pixels) if pixels > 0 else 1.0
        factor_dim_w = MAX_W / w if w > 0 else 1.0
        factor_dim_h = MAX_H / h if h > 0 else 1.0
        factor = min(1.0, factor_pixels, factor_dim_w, factor_dim_h)

        new_w = max(1, int(math.floor(w * factor)))
        new_h = max(1, int(math.floor(h * factor)))
        if (new_w, new_h) == (w, h):
            return {**input}

        out_name = f"clamped-{uuid.uuid4().hex}.mp4"
        out_path = os.path.join(TMP_DIR, out_name)

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        resized = clip.resize(newsize=(new_w, new_h))
        resized.write_videofile(
            out_path, codec="libx264", audio_codec="aac", threads=1, logger=None
        )

        resized.close()

    finally:
        clip.close()

    return {**input, "raw_file_path": input["file_path"], "file_path": out_path}


@worker_task(task_definition_name="tbnlr-sample-video")
def sample_video(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Sampling video frames...",
            client_id=input["client_id"],
        )
    )

    clip = VideoFileClip(input["file_path"])
    jpeg_paths = []
    try:
        duration = float(clip.duration) if clip.duration is not None else 0.0
        if duration <= 0:
            timestamps = [0.0 for _ in range(FRAME_COUNT)]
        else:
            timestamps = [
                ((i + 0.5) * duration / FRAME_COUNT) for i in range(FRAME_COUNT)
            ]

        for i, t in enumerate(timestamps, start=1):
            if duration > 0:
                t = max(0.0, min(t, max(0.0, duration - 1e-3)))
            frame = clip.get_frame(t)  # numpy array HxWx3 (RGB)
            out_jpeg = os.path.join(TMP_DIR, f"{JPEG_PREFIX}{i:02d}.jpg")
            imageio.imwrite(out_jpeg, frame, format="jpg")
            jpeg_paths.append(out_jpeg)
    finally:
        clip.close()

    return {**input, "jpeg_paths": jpeg_paths}


@worker_task(task_definition_name="tbnlr-save-to-gif")
def save_to_gif(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Saving frames into a GIF...",
            client_id=input["client_id"],
        )
    )

    images = [imageio.imread(p) for p in input["jpeg_paths"]]

    gif_path = os.path.join(TMP_DIR, GIF_FILENAME)
    imageio.mimsave(gif_path, images, format="GIF", duration=0.2)  # 1 fps
    zipfile_name = "{}.zip".format(input["client_id"])

    return {**input, "gif_path": gif_path, "tbnlr_doc": {"name": zipfile_name}}


@worker_task(task_definition_name="tbnlr-zip")
def zip_contents(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Zipping content...",
            client_id=input["client_id"],
        )
    )

    target_name = input["tbnlr_doc"]["name"]
    zip_local = os.path.join(TMP_DIR, target_name)
    parent = os.path.dirname(zip_local)
    if parent:
        os.makedirs(parent, exist_ok=True)

    files_to_add = []
    jpeg_paths = input.get("jpeg_paths", [])
    if jpeg_paths:
        files_to_add.extend(jpeg_paths)
    gif_path = input.get("gif_path")
    if gif_path:
        files_to_add.append(gif_path)

    if not files_to_add:
        raise ValueError(
            "Nothing to zip. Provide 'jpeg_paths' and/or 'gif_path' in input."
        )

    with ZipFile(zip_local, "w") as z:
        for f in files_to_add:
            if not os.path.exists(f):
                raise FileNotFoundError(f"Cannot add missing file to zip: {f}")
            z.write(f, arcname=os.path.basename(f))

    return {**input, "zip_path": zip_local}


@worker_task(task_definition_name="tbnlr-upload-s3")
def upload_s3(input: dict):
    notify(
        WSNotification(
            status=WorkflowStatus.RUNNING,
            message="Uploading zipped content to S3...",
            client_id=input["client_id"],
        )
    )

    with httpx.Client() as client:
        object_key = (
            f"{input['client_id']}-{input['tbnlr_doc']['name']}-{uuid.uuid4()}.zip"
        )
        s3_client = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
        )

        s3_client.upload_file(
            Filename=input["zip_path"],
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


@worker_task(task_definition_name="tbnlr-forward-url")
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
    os.remove("/tmp/" + input["tbnlr_doc"]["name"])
    os.remove(input["file_path"])

    return {
        **input,
    }
