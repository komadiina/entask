import json
import os

import google_auth_oauthlib.flow
import requests
import utils.auth as uauth
import urllib.parse
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, Response
import functions.auth

from constants.auth_responses import (
    InvalidClientResponse,
    InvalidRegistrationResponse,
    UnauthorizedResponse,
)
from models.auth import RegisterRequestModel, LoginRequestModel
from decorators.auth import authorized

API_PREFIX = f"/api/{os.environ.get('API_VERSION')}/auth"
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
async def oauth2_callback(code: str, state: str):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file=os.environ.get("CLIENT_SECRET_FILE"),
        scopes=SCOPES,
        state=state,
    )
    flow.redirect_uri = FLOW_REDIRECT_URI
    flow.fetch_token(code=code, state=state)

    id_token = flow.oauth2session.token.get("id_token")
    access_token = flow.credentials.token
    refresh_token = flow.credentials.refresh_token
    expiry = flow.credentials.expiry

    query = urllib.parse.urlencode(
        {
            "id_token": id_token,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expiry": expiry,
        }
    )
    url = f"{FRONTEND_HOST}/oauth2/callback?{query}"

    return RedirectResponse(url=url)


@auth_router.post("/register")
async def register_user(details: RegisterRequestModel):
    if details.is_incomplete():
        return InvalidRegistrationResponse("Missing required fields.")

    return functions.auth.register_user(details)


@auth_router.post("/login")
async def login_user(details: LoginRequestModel):
    print(details)
    res = functions.auth.login_user(details)
    print(res)
    return res


@auth_router.get("/me")
@authorized
async def get_user_details(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return UnauthorizedResponse()

    token = auth_header.split(" ")[1]

    print(token)

    res = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {token}"},
    )

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
