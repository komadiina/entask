import json
import os
import urllib.parse

import functions.auth
import google_auth_oauthlib.flow
import requests
import utils
import utils.auth as uauth
from constants.auth_responses import (
    InvalidClientResponse,
    InvalidRegistrationResponse,
    UnauthorizedResponse,
)
from decorators.auth import authorized
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse, Response
from models.auth import LoginRequestModel, RegisterRequestModel

API_PREFIX = f"/api/auth"
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
USES_HTTP = bool(os.getenv("TRAEFIK_USES_HTTP", False))
EXPOSED_PORT = (
    os.getenv("TRAEFIK_HTTP_PORT", 80)
    if USES_HTTP
    else os.getenv("TRAEFIK_HTTPS_PORT", 443)
)
FLOW_REDIRECT_URI = f"http://localhost:{EXPOSED_PORT}{API_PREFIX}/oauth2/callback"
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

    # get user details from google
    body = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    # save user to database
    functions.auth.register_user(
        RegisterRequestModel(
            given_name=body["given_name"],
            family_name=body["family_name"],
            email=body["email"],
            email_confirmed=body["email"],
            username=body["email"],
            password="<google-oauth2>",
            password_confirmed="<google-oauth2>",
        )
    )

    query = urllib.parse.urlencode(
        {
            "id_token": id_token,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expiry": expiry,
            "provider": "google",
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
    try:
        res = functions.auth.login_user(details)
        return res
    except HTTPException as e:
        return Response(
            content=json.dumps({"message": e.detail}), status_code=e.status_code
        )


@auth_router.get("/me")
@authorized
async def get_user_details(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return UnauthorizedResponse()

    credentials = utils.auth.get_credentials(request)
    email = utils.auth.get_email(request, credentials)
    user_details = functions.auth.get_user_details(email=email)

    if user_details is None:
        return Response(
            {"message": "User not found with the supplied credentials."},
            status_code=404,
        )

    return Response(content=user_details.model_dump_json())


@auth_router.post("/refresh-tokens")
@authorized
async def refresh_tokens(request: Request):
    access_token = request.headers.get("Authorization") or ""
    refresh_token = request.headers.get("x-refresh-token") or ""
    id_token = request.headers.get("x-id-token") or ""

    if access_token is not None or access_token != "":
        access_token = access_token.split(" ")[1]

    return functions.auth.refresh_credentials(
        {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "id_token": id_token,
        }
    )
