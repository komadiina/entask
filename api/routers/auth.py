import json
import os

import google_auth_oauthlib.flow
import requests
import utils.auth as uauth
import urllib.parse
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response

from constants.auth_responses import (
    InvalidClientResponse,
    InvalidJWTResponse,
    InvalidRegistrationResponse,
    UnauthorizedResponse,
)
from models.auth import RegisterRequestModel, LoginRequestModel

API_PREFIX = f"/api/{os.environ.get('API_VERSION')}/public/auth"
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
FLOW_REDIRECT_URI = (
    f"http://localhost:{os.environ.get('API_PORT')}{API_PREFIX}/oauth2/callback"
)
FRONTEND_HOST = (
    f"http://{os.environ.get('FRONTEND_HOST')}:{os.environ.get('FRONTEND_PORT')}"
)

auth_router = APIRouter(prefix=API_PREFIX)


@auth_router.get("/oauth2", response_class=Response)
async def oauth2(request: Request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file=os.environ.get("CLIENT_SECRET_FILE"),
        scopes=SCOPES,
    )

    flow.redirect_uri = FLOW_REDIRECT_URI
    auth_url, state = flow.authorization_url(
        include_granted_scopes="true",
        prompt="consent",
    )

    if request.client is not None:
        await uauth.save_temp_state(
            f"{request.client.host}{request.client.port}", state
        )
    else:
        return InvalidClientResponse()

    return RedirectResponse(url=auth_url)


@auth_router.get("/oauth2/callback", response_class=RedirectResponse)
async def oauth2_callback(request: Request, code: str, state: str):
    stored_state = ""
    if request.client is not None:
        stored_state = uauth.retrieve_temp_state(
            f"{request.client.host}{request.client.port}"
        )
    else:
        return InvalidClientResponse()

    # if state != stored_state:
    #     return InvalidCSRFTokenResponse()

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file=os.environ.get("CLIENT_SECRET_FILE"),
        scopes=SCOPES,
        state=state,
    )
    flow.redirect_uri = FLOW_REDIRECT_URI
    flow.fetch_token(code=code, state=state)

    query = urllib.parse.urlencode(
        {
            "access_token": flow.credentials.token,
            "refresh_token": flow.credentials.refresh_token or "",
            "expiry": flow.credentials.expiry.isoformat(),  # pyright: ignore[reportOptionalMemberAccess]
        }
    )
    url = f"{FRONTEND_HOST}/oauth2/callback?{query}"

    return RedirectResponse(url=url)


@auth_router.post("/register")
async def register_user(request: Request, details: RegisterRequestModel):
    if details.is_incomplete():
        return InvalidRegistrationResponse("Missing required fields.")

    return uauth.register_user(details)


@auth_router.post("/login")
async def login_user(request: Request, details: LoginRequestModel):
    return uauth.check_login(details)


@auth_router.get("/auth/me")
async def get_user_details(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return UnauthorizedResponse()

    token = auth_header.split(" ")[1]

    res = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {token}"},
    )

    if res.status_code != 200:
        return InvalidJWTResponse()

    body = res.json()

    return Response(
        content=json.dumps(
            {
                "name": body["name"],
                "email": body["email"],
                "picture": body["picture"],
            }
        )
    )
