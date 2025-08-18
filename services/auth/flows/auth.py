import os

import fastapi
import google.oauth2.id_token
import jwt
import models.auth
from google.auth.transport import requests as grequests


def google_oauth2_flow(request: fastapi.Request) -> models.auth.Credentials:
    # TODO check for presence of x-refresh/access/id tokens

    payload = google.oauth2.id_token.verify_oauth2_token(
        request.headers.get("x-id-token"),
        grequests.Request(),
        os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
        clock_skew_in_seconds=60,
    )

    return models.auth.Credentials(
        access_token=request.headers.get("x-access-token") or "",
        refresh_token=request.headers.get("x-refresh-token") or "",
        id_token=request.headers.get("x-id-token") or "",
        access_token_expiry=payload["exp"],
        refresh_token_expiry=payload["exp"],
    )


def entask_auth_flow(request: fastapi.Request) -> models.auth.Credentials:
    if request is None:
        raise ValueError("property 'request' cannot be of NoneType")

    if request.headers is None:
        raise ValueError("property 'request.headers' cannot be of NoneType")

    access_token = request.headers.get("Authorization") or ""
    refresh_token = request.headers.get("x-refresh-token") or ""
    id_token = request.headers.get("x-id-token") or ""

    decoded_at = jwt.decode(
        access_token,
        os.environ.get("JWT_SECRET_KEY") or "",
        algorithms=[os.environ.get("JWT_ALGORITHM") or ""],
    )

    return models.auth.Credentials(
        access_token=access_token,
        refresh_token=refresh_token,
        id_token=id_token,
        access_token_expiry=decoded_at["claims"]["exp"],
        refresh_token_expiry=decoded_at["claims"]["exp"],
    )
