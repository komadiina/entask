import os
from logging import getLogger
from typing import Any

import psycopg
from psycopg import Connection
from psycopg.errors import ProgrammingError
from psycopg.rows import DictRow, dict_row
from psycopg.sql import SQL, Composed, Identifier

user = os.getenv("AUTH_DB_USER")
password = os.getenv("AUTH_DB_PASSWORD")
host = os.getenv("AUTH_DB_HOST")
port = os.getenv("AUTH_DB_PORT")
database = os.getenv("AUTH_DB", "auth")
conninfo = "postgresql://{}:{}@{}:{}/{}".format(user, password, host, port, database)


logger = getLogger(__name__)
logger.info(f"Initialized connection string: {conninfo}")


def get_connection() -> Connection[Any]:
    return psycopg.connect(conninfo=conninfo)


def exec_query(
    sql: SQL | Composed, params: tuple | None, produces_results: bool = False
) -> list[DictRow] | None:
    """Executes a parametrized (composed) query.

    Args:
        sql (SQL | Composed): SQL-formatted query, using `psycopg.sql.SQL`.
        params (tuple): Query parameters (ordered).

    Returns:
        (list[DictRow] | None): The result set (if query is of SELECT type), else `None`.
    """

    def close(cursor: psycopg.Cursor[Any], conn: psycopg.Connection[Any]):
        cursor.close()
        conn.close()

    with psycopg.connect(conninfo=conninfo) as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            try:
                cursor.execute(
                    SQL("SET search_path TO {};").format(Identifier(database))
                )
                logger.info(f"SQL: {sql}; params: {params}")
                cursor.execute(sql, params or ())

                if produces_results:
                    return cursor.fetchall()

                conn.commit()
                return None
            except (Exception, ProgrammingError) as e:
                logger.exception(e)
                return None
            finally:
                close(cursor, conn)


def close_connection(conn: psycopg.Connection) -> None:
    conn.close()
    return
