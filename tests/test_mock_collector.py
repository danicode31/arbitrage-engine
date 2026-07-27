from src.collectors.mock import MockCollector


def test_mock_collector_returns_quotes() -> None:
    collector = MockCollector()

    quotes = collector.get_quotes()

    assert len(quotes) == 5
    assert {quote.symbol for quote in quotes} == {
        "GGAL",
        "YPFD",
        "PAMP",
        "TXAR",
        "AL30",
    }


def test_mock_quotes_have_valid_spread() -> None:
    collector = MockCollector()

    quotes = collector.get_quotes()

    for quote in quotes:
        assert quote.ask >= quote.bid
        assert quote.spread > 0
