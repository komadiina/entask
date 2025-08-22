import logging
import mimetypes
import os
import uuid

import boto3
import httpx
from fastapi import FastAPI, Query, Request
from models.presign import PresignRequest

S3_ENDPOINT = "http://{}:{}".format(
    os.getenv("S3_HOST", "minio"),
    os.getenv("S3_PORT", 9000),
)
S3_BUCKET_UPLOADS = os.getenv("S3_UPLOAD_BUCKET", "uploads")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
URI_TTL = int(os.getenv("URI_TTL", 300))


app = FastAPI()
s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
)
logger = logging.getLogger(__name__)


@app.get("/api/file/version")
async def version():
    return {
        "service": "file-service",
        "version": os.getenv("FILE_API_VERSION", "v1"),
    }


@app.get("/api/file/health")
async def health():
    return {"status": "ok"}


@app.post("/api/presign/upload")
async def create_upload_url(req: PresignRequest):
    """Creates an upload url for object in key format: `uploads/<conversion_type>/{username}-{filename}-{uuid4}.{ext}`,

    Args:
        req (PresignRequest): Request body schema, see `models.presign.PresignRequest`

    Raises:
        httpx.HTTPStatusError: If contacting the `auth-service` failed for any reason given.

    """

    # contact auth-service to get username
    user_id = None
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(
                "http://{}:{}/api/auth/user/me".format(
                    os.getenv("AUTH_API_HOST"),
                    os.getenv("AUTH_SERVICE_PORT"),
                )
            )
            if res.status_code != 200:
                raise httpx.HTTPStatusError(
                    request=res.request, response=res, message="failed fetching user_id"
                )

            user_id = res.json().get("username")
        except httpx.RequestError as e:
            logger.exception(
                "failed fetching user_id, using 'anonymous'",
                extra={"error": str(e)},
            )
            user_id = "anonymous"

    # find file ext
    ext = os.path.splitext(req.filename)[1]
    if not ext:
        ext = mimetypes.guess_extension("application/octet-stream") or ""

    # fetch s3 object key
    object_key = f"uploads/{req.conversion_type}/{user_id}-{req.filename}-{uuid.uuid4().hex}{ext}"

    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": S3_BUCKET_UPLOADS,
            "Key": object_key,
            "ContentType": mimetypes.guess_type(req.filename)[0]
            or "application/octet-stream",
        },
        ExpiresIn=URI_TTL,
    )
    return {"url": presigned_url, "bucket": S3_BUCKET_UPLOADS, "key": object_key}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("FILE_SERVICE_PORT", 5203)))
