import logging
import mimetypes
import os
import uuid

import boto3
import httpx
from fastapi import APIRouter, Query, Request
from models.presign import PresignRequest

S3_HOST = os.getenv("S3_HOST", "minio")
S3_PORT = os.getenv("S3_PORT", 9000)
S3_ENDPOINT = "http://{}:{}".format(S3_HOST, S3_PORT)
S3_BUCKET_UPLOADS = os.getenv("S3_BUCKET_UPLOADS", "uploads")
S3_BUCKET_CONVERSIONS = os.getenv("S3_BUCKET_CONVERSIONS", "conversions")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
URI_TTL = int(os.getenv("URI_TTL", "300"))


file_router = APIRouter(prefix="/api/file")
s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
)
logger = logging.getLogger(__name__)


@file_router.get("/presign/upload/converted")
async def create_upload_url_converted(
    request: Request,
    filename: str,
    conversion_type: str,
    file_mime_type: str,
    use_localhost: bool = True,
):
    # TODO
    return await create_upload_url(
        request, filename, conversion_type, file_mime_type, use_localhost
    )


@file_router.get("/presign/upload")
async def create_upload_url(
    request: Request,
    filename: str,
    conversion_type: str,
    file_mime_type: str,
    use_localhost: bool = True,
    use_auth: bool = True,
):
    """Creates an upload url for object in key format: `uploads/<conversion_type>/{username}-{filename}-{uuid4}.{ext}`,

    Args:
        req (PresignRequest): Request body schema, see `models.presign.PresignRequest`

    Raises:
        httpx.HTTPStatusError: If contacting the `auth-service` failed for any reason given.

    """

    # contact auth-service to get email
    user_id = None

    if use_auth:
        async with httpx.AsyncClient() as client:
            try:
                AUTH_SERVICE_PORT = os.getenv("AUTH_SERVICE_PORT")
                AUTH_SERVICE_HOST = os.getenv("AUTH_SERVICE_HOST")

                ### todo: migrated from POST to GET request, revise this later
                # forwarding POST headers, change 'Content-Length' to '0' (no body)
                headers = request.headers.mutablecopy()
                headers["Content-Length"] = "0"

                res = await client.get(
                    "http://{}:{}/api/auth/me".format(
                        AUTH_SERVICE_HOST, AUTH_SERVICE_PORT
                    ),
                    headers=headers,
                )
                if res.status_code != 200:
                    raise httpx.HTTPStatusError(
                        request=res.request,
                        response=res,
                        message="failed fetching user_id",
                    )

                user_id = res.json().get("email")
            except httpx.RequestError as e:
                logger.exception(
                    "failed fetching user_id, using 'anonymous'",
                    extra={"error": str(e)},
                )
                user_id = "anonymous@unknown.com"
    else:
        user_id = "conversion-response"

    # find file ext
    ext = os.path.splitext(filename)[1]
    if not ext:
        ext = mimetypes.guess_extension("application/octet-stream") or ""

    # fetch s3 object key
    object_key = f"{conversion_type}/{user_id}-{filename}-{uuid.uuid4().hex}{ext}"

    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": S3_BUCKET_UPLOADS,
            "ContentType": file_mime_type,
            "Key": object_key,
        },
        ExpiresIn=URI_TTL,
    )
    return {
        "url": (
            presigned_url.replace(S3_HOST, "localhost")
            if use_localhost
            else presigned_url
        ),
        "bucket": S3_BUCKET_UPLOADS,
        "key": object_key,
        "user_id": user_id,
    }


@file_router.post("/presign/download/raw")
async def get_raw_document(request: Request):
    object_key = (await request.json())["object_key"]

    presigned_url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": S3_BUCKET_UPLOADS,
            "Key": object_key,
        },
        ExpiresIn=URI_TTL,
    )

    return {"url": presigned_url}


@file_router.get("/presign/download")
async def get_download_url(object_key: str):
    presigned_url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": S3_BUCKET_CONVERSIONS,
            "Key": object_key,
        },
        ExpiresIn=URI_TTL,
    )

    return {
        "url": presigned_url.replace(
            "localhost",
        )
    }
