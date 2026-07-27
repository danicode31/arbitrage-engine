import pytest

from src.collectors.mock import MockCollector


def test_mock_collector_connection_state() -> None:
    collector = MockCollector()

    assert collector.is_connected is False

    collector.connect()

    assert collector.is_connected is True

    collector.disconnect()

    assert collector.is_connected is False


def test_mock_collector_returns_quotes() -> None:
    collector = MockCollector()
    collector.connect()

    quotes = collector.get_quotes()

    assert len(quotes) == 5
    assert {quote.symbol for quote in quotes} == {
        "GGAL",
        "YPFD",
        "PAMP",
        "TXAR",
        "AL30",
    }


def test_mock_collector_requires_connection() -> None:
    collector = MockCollector()

    with pytest.raises(
        RuntimeError,
        match="debe estar conectado",
    ):
        collector.get_quotes()


def test_mock_quotes_have_valid_spread() -> None:
    collector = MockCollector()
    collector.connect()

    quotes = collector.get_quotes()

    for quote in quotes:
        assert quote.ask >= quote.bid
        assert quote.spread > 0
