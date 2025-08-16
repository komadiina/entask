import os

import psycopg
from psycopg import Connection
from psycopg.errors import ProgrammingError
from psycopg.rows import DictRow, dict_row
from psycopg.sql import SQL, Composed
from psycopg_pool.pool import ConnectionPool

user = os.environ["PGSQL_USER"]
password = os.environ["PGSQL_PASSWORD"]
host = os.environ["PGSQL_HOST"]
port = os.environ["PGSQL_PORT"]
database = os.environ["PGSQL_DATABASE"]
conn_str = f"postgresql://{user}:{password}@{host}:{port}/{database}"

pool = ConnectionPool(
    conninfo=conn_str,
    min_size=6,
    open=True,
    num_workers=4,
    kwargs={"row_factory": dict_row},
)


# TODO: threads asyncio running loop
# async_pool = AsyncConnectionPool(
#     conninfo=conn_str,
#     min_size=6,
#     open=True,
#     num_workers=4,
#     kwargs={"row_factory": dict_row},
# )


def get_connection() -> Connection[DictRow]:
    return pool.getconn()


def exec_query(sql: SQL | Composed, params: tuple | None) -> list[DictRow] | None:
    """Executes a parametrized (composed) query.

    Args:
        sql (SQL | Composed): SQL-formatted query, using `psycopg.sql.SQL`.
        params (tuple): Query parameters (ordered).

    Returns:
        (list[DictRow] | None): The result set (if query is of SELECT type), else `None`.
    """
    with pool.connection() as conn:
        conn.execute(SQL("SET search_path TO {schema};").format(schema=database))
        try:
            cursor = conn.execute(sql, params)
            result_set = cursor.fetchall()
            return result_set
        except ProgrammingError as e:
            # thrown from fetchall() method - can't fetch on produced empty records
            return None


def close_connection(conn: psycopg.Connection) -> None:
    conn.close()
    return
