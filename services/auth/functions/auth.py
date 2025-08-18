import os
from datetime import datetime
from typing import Any, Dict

import bcrypt
from fastapi.exceptions import HTTPException
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWSSignatureError
from models.auth import Credentials, LoginRequestModel, RegisterRequestModel
from models.db.user import User
from psycopg import sql
from utils.auth import check_password, generate_credentials
from utils.pgsql import exec_query

BCRYPT_EFF = 16


def refresh_credentials(tokens: Dict[str, str]) -> Credentials:
    try:
        decoded_atoken = jwt.decode(
            tokens["access_token"],
            os.environ.get("JWT_SECRET_KEY") or "",
            algorithms=[os.environ.get("JWT_ALGORITHM") or "HS256"],
        )

        decoded_rtoken = jwt.decode(
            tokens["refresh_token"],
            os.environ.get("JWT_REFRESH_KEY") or "",
            algorithms=[os.environ.get("JWT_ALGORITHM") or "HS256"],
        )

        decoded_itoken = jwt.decode(
            tokens["id_token"],
            os.environ.get("JWT_OIDC_KEY") or "",
            algorithms=[os.environ.get("JWT_ALGORITHM") or "HS256"],
        )

        if decoded_atoken["claims"]["sub"] != decoded_rtoken["claims"]["sub"]:
            raise HTTPException(status_code=401, detail="Invalid tokens supplied.")

        if (
            decoded_atoken["claims"]["type"] != "access"
            or decoded_rtoken["claims"]["type"] != "refresh"
            or decoded_itoken["claims"]["type"] != "oidc"
        ):
            raise HTTPException(status_code=401, detail="Invalid tokens supplied.")

        if decoded_atoken["claims"]["exp"] < datetime.now().timestamp():
            if decoded_rtoken["claims"]["exp"] < datetime.now().timestamp():
                raise HTTPException(status_code=401, detail="Refresh token expired")
            else:
                return generate_credentials(
                    decoded_atoken["claims"]["sub"], decoded_atoken["claims"]["email"]
                )
        else:
            raise HTTPException(status_code=401, detail="Access token expired.")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired.")
    except JWSSignatureError:
        raise HTTPException(status_code=401, detail="Invalid signature received.")


def register_user(user: RegisterRequestModel) -> Dict[str, Any]:

    # check if user already exists (username && email criteria)
    q = sql.SQL(
        "select * from {table} where {username} LIKE %s OR {email} LIKE %s;"
    ).format(
        table=sql.Identifier("users"),
        username=sql.Identifier("username"),
        email=sql.Identifier("email"),
    )

    result = exec_query(q, (user.username, user.email))

    if result is not None and len(result) > 0:
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        q = sql.SQL(
            "INSERT INTO {table} ({columns}) VALUES (%s, %s, %s, %s, %s);"
        ).format(
            table=sql.Identifier("users"),
            columns=sql.SQL(", ").join(
                map(
                    sql.Identifier,
                    ["username", "email", "given_name", "family_name", "password"],
                )
            ),
        )

        result = exec_query(
            q,
            (
                user.username,
                user.email,
                user.given_name,
                user.family_name,
                bcrypt.hashpw(
                    user.password.encode("utf-8"), bcrypt.gensalt(BCRYPT_EFF)
                ).decode("utf-8"),
            ),
        )

    except RuntimeError as e:
        raise HTTPException(status_code=400, detail="Unable to register user.")

    return {"message": "User registered successfully"}


def login_user(user: LoginRequestModel):
    # check if user already exists (username && email criteria)
    q = sql.SQL("SELECT * FROM {table} WHERE {v1} LIKE %s OR {v2} LIKE %s;").format(
        table=sql.Identifier("users"),
        v1=sql.Identifier("username"),
        v2=sql.Identifier("email"),
    )

    result = exec_query(q, (user.username_email, user.username_email))

    if result is not None and len(result):
        for row in result:
            if check_password(user.password, row["password"]):
                return generate_credentials(row["username"], row["email"])

    raise HTTPException(status_code=400, detail="User does not exist")


def get_user_details(email: str) -> User | None:
    result = exec_query(
        sql=sql.SQL("SELECT * FROM {table} WHERE {v1} LIKE %s;").format(
            table=sql.Identifier("users"),
            v1=sql.Identifier("email"),
        ),
        params=(email),
    )

    if result is not None and len(result):
        for row in result:
            return User(**row)

    return None
