from pathlib import Path

import pytest

from src.core.database import Database


def test_database_connection(tmp_path: Path) -> None:
    database_path = tmp_path / "test_arbitrage.db"
    database = Database(str(database_path))

    assert database.is_connected is False

    database.connect()

    assert database.is_connected is True

    database.disconnect()

    assert database.is_connected is False


def test_database_requires_connection(tmp_path: Path) -> None:
    database = Database(str(tmp_path / "test_arbitrage.db"))

    with pytest.raises(
        RuntimeError,
        match="no está conectada",
    ):
        _ = database.connection


def test_database_initialization(tmp_path: Path) -> None:
    database = Database(str(tmp_path / "test_arbitrage.db"))

    database.connect()
    database.initialize()

    result = database.connection.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_name = 'market_quotes'
        """
    ).fetchone()

    database.disconnect()

    assert result is not None
    assert result[0] == "market_quotes"
