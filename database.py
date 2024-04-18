import MySQLdb
import logging
from typing import Any, Dict, List

# Setup logging
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages connections and operations with a MySQL database."""

    def __init__(self, host: str, user: str, password: str, db: str):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.connection = self.connect()

    def connect(self) -> MySQLdb.connections.Connection:
        """Establishes a connection to the database."""
        try:
            connection = MySQLdb.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                db=self.db
            )
            logger.info("Database connection established")
            return connection
        except MySQLdb.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Executes a query and returns the results."""
        with self.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_update(self, query: str, params: Dict[str, Any] = None) -> None:
        """Executes an update query."""
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()

    def close(self) -> None:
        """Closes the database connection."""
        self.connection.close()
        logger.info("Database connection closed")

    def __del__(self):
        self.close()
