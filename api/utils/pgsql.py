import os
from typing import Any

import psycopg


def get_connection() -> psycopg.Connection:
    conn = psycopg.connect(
        user=os.environ.get("PGSQL_USER"),
        password=os.environ.get("PGSQL_PASSWORD"),
        host=os.environ.get("PGSQL_HOST"),
        port=os.environ.get("PGSQL_PORT"),
        dbname=os.environ.get("PGSQL_DATABASE"),
        options=f"-c search_path={os.environ.get("PGSQL_DATABASE")}",
    )
    return conn


def close_connection(conn: psycopg.Connection) -> None:
    conn.close()
    return


def get_cursor(conn: psycopg.Connection) -> psycopg.Cursor[Any]:
    return conn.cursor()


def close_cursor(cur: psycopg.Cursor) -> None:
    cur.close()
    return
