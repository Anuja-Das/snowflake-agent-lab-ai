import pandas as pd
import snowflake.connector
from src.utils import get_logger

logger = get_logger(__name__)


class QueryExecutor:
    """Executes SQL queries against a Snowflake connection."""

    def __init__(self, conn: snowflake.connector.SnowflakeConnection):
        self._conn = conn

    def execute(self, sql: str, params: tuple = None) -> list[dict]:
        with self._conn.cursor(snowflake.connector.DictCursor) as cur:
            cur.execute(sql, params)
            results = cur.fetchall()
            logger.debug("Query returned {} rows", len(results))
            return results

    def execute_to_df(self, sql: str, params: tuple = None) -> pd.DataFrame:
        with self._conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetch_pandas_all()

    def execute_many(self, sql: str, data: list[tuple]) -> int:
        with self._conn.cursor() as cur:
            cur.executemany(sql, data)
            logger.info("Inserted {} rows", cur.rowcount)
            return cur.rowcount

    def load_df(self, df: pd.DataFrame, table: str, database: str, schema: str) -> None:
        from snowflake.connector.pandas_tools import write_pandas
        success, nchunks, nrows, _ = write_pandas(
            self._conn, df, table, database=database, schema=schema
        )
        if success:
            logger.info("Loaded {} rows into {}.{}.{}", nrows, database, schema, table)
        else:
            raise RuntimeError(f"write_pandas failed for table {table}")
