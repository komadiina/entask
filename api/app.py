import json

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import google_auth_oauthlib.flow
import logging
import os
from typing import Optional

# TODO: testing, [[REMOVE]] in prod
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

logger = logging.getLogger()
app = FastAPI()
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email'
]
app.state.credentials = []
STATE = ''

@app.get('/hello')
async def hello():
    return {'message': 'hello'}


@app.get('/oauth2', response_class=RedirectResponse)
async def oauth2(request: Request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file='./secrets/client_secret.json',
        scopes=SCOPES,
    )

    flow.redirect_uri = "http://localhost:4201/oauth2/callback"
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    STATE = state
    print(f"state: {state}")

    return auth_url


@app.get('/oauth2/callback')
async def oauth2_callback(request: Request, code: Optional[str]):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file="./secrets/client_secret.json",
        scopes=SCOPES,
        state=STATE
    )
    flow.redirect_uri = 'http://localhost:4201/oauth2/callback'

    print(f"--> {code}")

    flow.fetch_token(code=code, state=STATE)
    app.state.credentials = [*app.state.credentials, flow.credentials]

    return {
        "destination": "http://localhost:4200/dashboard",
        "credentials": {
            "client_id": flow.credentials.client_id,
            "scopes": flow.credentials.scopes,
            "token_uri": flow.client_config.get("token_uri"),
            "token": flow.credentials.token,
            "refresh_token": flow.credentials.refresh_token,
            "expiry": flow.credentials.expiry
        }
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=4201)
