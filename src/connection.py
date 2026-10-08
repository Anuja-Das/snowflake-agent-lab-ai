import os
import snowflake.connector
from dotenv import load_dotenv
from src.utils import get_logger

load_dotenv()
logger = get_logger(__name__)


class SnowflakeConnection:
    """Manages a Snowflake connection using environment variables."""

    def __init__(self):
        self._conn = None

    def connect(self) -> snowflake.connector.SnowflakeConnection:
        self._conn = snowflake.connector.connect(
            account=os.environ["SNOWFLAKE_ACCOUNT"],
            user=os.environ["SNOWFLAKE_USER"],
            password=os.environ["SNOWFLAKE_PASSWORD"],
            warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
            database=os.environ.get("SNOWFLAKE_DATABASE"),
            schema=os.environ.get("SNOWFLAKE_SCHEMA"),
            role=os.environ.get("SNOWFLAKE_ROLE"),
        )
        logger.info("Connected to Snowflake account: {}", os.environ["SNOWFLAKE_ACCOUNT"])
        return self._conn

    def close(self):
        if self._conn and not self._conn.is_closed():
            self._conn.close()
            logger.info("Snowflake connection closed")

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
