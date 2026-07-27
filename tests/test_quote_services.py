from pathlib import Path

import pytest

from src.collectors.base import BaseCollector
from src.collectors.mock import MockCollector
from src.core.database import Database
from src.events.event_bus import EventBus
from src.events.market_events import QuotesCollectedEvent
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
        event_bus=EventBus(),
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
        event_bus=EventBus(),
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
        event_bus=EventBus(),
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


def test_quote_service_publishes_event(
    tmp_path: Path,
) -> None:
    database = Database(str(tmp_path / "test_arbitrage.db"))
    database.connect()
    database.initialize()

    repository = MarketQuoteRepository(database)
    event_bus = EventBus()
    received_events: list[QuotesCollectedEvent] = []

    def handler(event: QuotesCollectedEvent) -> None:
        received_events.append(event)

    event_bus.subscribe(
        QuotesCollectedEvent,
        handler,
    )

    service = QuoteService(
        collector=MockCollector(),
        repository=repository,
        event_bus=event_bus,
    )

    service.collect()

    assert len(received_events) == 1
    assert len(received_events[0].quotes) == 5

    database.disconnect()
