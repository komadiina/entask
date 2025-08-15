from sqlite3 import Row
from utils.pgsql import *
from utils.auth import check_password, generate_credentials
import bcrypt
from models.auth import LoginRequestModel, RegisterRequestModel
from fastapi.exceptions import HTTPException
from typing import Dict, Any, Sequence

BCRYPT_EFF = 16


def register_user(user: RegisterRequestModel) -> Dict[str, Any]:
    # open pgsql connection
    conn = get_connection()
    cur = get_cursor(conn)

    # check if user already exists (username && email criteria)
    cur = cur.execute(
        query="SELECT * FROM users WHERE username = %s OR email = %s;",
        params=(user.username, user.email),
    )
    result = cur.fetchall()
    if len(result) > 0:
        raise HTTPException(status_code=400, detail="User already exists")

    # save into pgsql 'users' table
    cur = cur.execute(
        query="INSERT INTO users (username, email, given_name, family_name, password) VALUES (%s, %s, %s, %s, %s);",
        params=(
            user.username,
            user.email,
            user.given_name,
            user.family_name,
            bcrypt.hashpw(
                user.password.encode("utf-8"), bcrypt.gensalt(BCRYPT_EFF)
            ).decode("utf-8"),
        ),
    )
    conn.commit()
    close_connection(conn)

    return {"message": "User registered successfully"}


def login_user(user: LoginRequestModel):
    # open pgsql connection
    conn = get_connection()
    cur = get_cursor(conn)

    # check if user already exists (username && email criteria)
    cur = cur.execute(
        query="SELECT * FROM users WHERE username LIKE %s OR email LIKE %s;",
        params=(user.username_email, user.username_email),
    )
    result = cur.fetchall()
    print(result)
    if len(result):
        for row in result:
            if check_password(user.password, row["password"]):
                return generate_credentials(user)

    raise HTTPException(status_code=400, detail="User does not exist")
