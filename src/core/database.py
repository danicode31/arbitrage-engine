from pathlib import Path

import duckdb
from duckdb import DuckDBPyConnection

from src.core.config import BASE_DIR, settings
from src.core.logger import get_logger

logger = get_logger(__name__)


class Database:
    """Administra la conexión local con DuckDB."""

    def __init__(self, database_path: str | None = None) -> None:
        relative_path = database_path or settings.database_path
        self.database_path = BASE_DIR / Path(relative_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

        self._connection: DuckDBPyConnection | None = None

    @property
    def connection(self) -> DuckDBPyConnection:
        if self._connection is None:
            raise RuntimeError("La base de datos no está conectada.")

        return self._connection

    @property
    def is_connected(self) -> bool:
        return self._connection is not None

    def connect(self) -> None:
        if self.is_connected:
            logger.warning("DuckDB ya estaba conectado.")
            return

        self._connection = duckdb.connect(str(self.database_path))
        logger.info("DuckDB conectado en %s", self.database_path)

    def disconnect(self) -> None:
        if not self.is_connected:
            logger.warning("DuckDB ya estaba desconectado.")
            return

        self.connection.close()
        self._connection = None
        logger.info("DuckDB desconectado.")

    def initialize(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS market_quotes (
                symbol VARCHAR NOT NULL,
                market VARCHAR NOT NULL,
                bid DECIMAL(18, 6) NOT NULL,
                ask DECIMAL(18, 6) NOT NULL,
                last DECIMAL(18, 6) NOT NULL,
                bid_size DECIMAL(18, 6) NOT NULL,
                ask_size DECIMAL(18, 6) NOT NULL,
                timestamp TIMESTAMPTZ NOT NULL
            )
            """
        )

        logger.info("Tabla market_quotes inicializada.")
