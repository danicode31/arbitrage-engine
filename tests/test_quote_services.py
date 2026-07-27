from pathlib import Path

import pytest

from src.collectors.base import BaseCollector
from src.collectors.mock import MockCollector
from src.core.database import Database
from src.models.market import MarketQuote
from src.services.quote_services import QuoteService
from src.storage.market_quote_repository import MarketQuoteRepository


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
        raise RuntimeError("Error simulado del collector")


def test_quote_service_collects_and_persists_quotes(
    tmp_path: Path,
) -> None:
    database = Database(str(tmp_path / "test_arbitrage.db"))
    database.connect()
    database.initialize()

    repository = MarketQuoteRepository(database)
    collector = MockCollector()

    service = QuoteService(
        collector=collector,
        repository=repository,
    )

    quotes = service.collect()

    assert len(quotes) == 5
    assert repository.count() == 5
    assert len(service.latest_quotes()) == 5
    assert collector.is_connected is False

    database.disconnect()


def test_latest_quotes_returns_a_copy(
    tmp_path: Path,
) -> None:
    database = Database(str(tmp_path / "test_arbitrage.db"))
    database.connect()
    database.initialize()

    repository = MarketQuoteRepository(database)

    service = QuoteService(
        collector=MockCollector(),
        repository=repository,
    )

    service.collect()

    returned_quotes = service.latest_quotes()
    returned_quotes.clear()

    assert len(service.latest_quotes()) == 5

    database.disconnect()


def test_quote_service_disconnects_when_collection_fails(
    tmp_path: Path,
) -> None:
    database = Database(str(tmp_path / "test_arbitrage.db"))
    database.connect()
    database.initialize()

    repository = MarketQuoteRepository(database)
    collector = FailingCollector()

    service = QuoteService(
        collector=collector,
        repository=repository,
    )

    with pytest.raises(
        RuntimeError,
        match="Error simulado",
    ):
        service.collect()

    assert collector.is_connected is False
    assert repository.count() == 0
    assert service.latest_quotes() == []

    database.disconnect()
