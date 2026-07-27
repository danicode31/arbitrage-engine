from pathlib import Path

import pytest

from src.collectors.base import BaseCollector
from src.collectors.mock import MockCollector
from src.core.database import Database
from src.models.market import MarketQuote
from src.services.market_pipeline import MarketPipeline
from src.storage.market_quote_repository import MarketQuoteRepository


def test_market_pipeline_collects_and_saves_quotes(
    tmp_path: Path,
) -> None:
    database = Database(str(tmp_path / "test_arbitrage.db"))
    database.connect()
    database.initialize()

    repository = MarketQuoteRepository(database)
    collector = MockCollector()

    pipeline = MarketPipeline(
        collector=collector,
        repository=repository,
    )

    processed_quotes = pipeline.run()

    assert processed_quotes == 5
    assert repository.count() == 5
    assert collector.is_connected is False

    database.disconnect()


class FailingCollector(BaseCollector):
    def __init__(self) -> None:
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

    def connect(self) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def get_quotes(self) -> list[MarketQuote]:
        raise RuntimeError("Error simulado del proveedor")


def test_market_pipeline_disconnects_on_error(
    tmp_path: Path,
) -> None:
    database = Database(str(tmp_path / "test_arbitrage.db"))
    database.connect()
    database.initialize()

    repository = MarketQuoteRepository(database)
    collector = FailingCollector()

    pipeline = MarketPipeline(
        collector=collector,
        repository=repository,
    )

    with pytest.raises(
        RuntimeError,
        match="Error simulado",
    ):
        pipeline.run()

    assert collector.is_connected is False
    assert repository.count() == 0

    database.disconnect()
