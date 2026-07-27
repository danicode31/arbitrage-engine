from decimal import Decimal

from src.models.market import MarketQuote
from src.services.arbitrage_engine import ArbitrageEngine
from src.strategies.cross_market import CrossMarketArbitrageStrategy


def test_engine_detects_opportunity() -> None:
    quotes = [
        MarketQuote(
            symbol="GGAL",
            market="BYMA",
            bid=Decimal("8190"),
            ask=Decimal("8200"),
            last=Decimal("8195"),
            bid_size=100,
            ask_size=100,
        ),
        MarketQuote(
            symbol="GGAL",
            market="NYSE",
            bid=Decimal("8350"),
            ask=Decimal("8360"),
            last=Decimal("8355"),
            bid_size=100,
            ask_size=100,
        ),
    ]

    engine = ArbitrageEngine(strategies=[CrossMarketArbitrageStrategy()])

    opportunities = engine.analyze(quotes)

    assert len(opportunities) == 1
    assert opportunities[0].gross_spread == Decimal("150")
    assert opportunities[0].is_profitable


def test_engine_returns_empty_list_without_spread() -> None:
    quotes = [
        MarketQuote(
            symbol="GGAL",
            market="BYMA",
            bid=Decimal("8190"),
            ask=Decimal("8200"),
            last=Decimal("8195"),
            bid_size=100,
            ask_size=100,
        ),
        MarketQuote(
            symbol="GGAL",
            market="NYSE",
            bid=Decimal("8180"),
            ask=Decimal("8190"),
            last=Decimal("8185"),
            bid_size=100,
            ask_size=100,
        ),
    ]

    engine = ArbitrageEngine(strategies=[CrossMarketArbitrageStrategy()])

    opportunities = engine.analyze(quotes)

    assert opportunities == []
