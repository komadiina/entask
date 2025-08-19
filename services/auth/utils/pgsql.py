import os
from typing import Any

import psycopg
from psycopg import Connection, Cursor
from psycopg.errors import ProgrammingError
from psycopg.rows import DictRow, RowMaker, dict_row
from psycopg.sql import SQL, Composed

user = os.environ["AUTH_DB_USER"]
password = os.environ["AUTH_DB_PASSWORD"]
host = os.environ["AUTH_DB_HOST"]
port = os.environ["AUTH_DB_PORT"]
database = os.environ["AUTH_DB"]
conn_str = f"postgresql://{user}:{password}@{host}:{port}/{database}"


def get_connection() -> Connection[Any]:
    return psycopg.connect(conn_str)


def exec_query(sql: SQL | Composed, params: tuple | str | None) -> list[DictRow] | None:
    """Executes a parametrized (composed) query.

    Args:
        sql (SQL | Composed): SQL-formatted query, using `psycopg.sql.SQL`.
        params (tuple): Query parameters (ordered).

    Returns:
        (list[DictRow] | None): The result set (if query is of SELECT type), else `None`.
    """
    conn = get_connection()
    cursor = conn.cursor(row_factory=dict_row)
    cursor.execute(SQL("SET search_path TO {schema};").format(schema=database))

    try:
        cursor = cursor.execute(sql, params)
        result_set = cursor.fetchall()
        cursor.close()
        conn.close()

        return result_set
    except ProgrammingError as e:
        # thrown from fetchall() method - can't fetch on produced empty records
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

        return None


def close_connection(conn: psycopg.Connection) -> None:
    conn.close()
    return
