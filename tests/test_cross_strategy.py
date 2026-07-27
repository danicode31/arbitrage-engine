from decimal import Decimal

from src.models.market import MarketQuote
from src.strategies.cross_market import CrossMarketArbitrageStrategy


def create_quote(
    symbol: str,
    market: str,
    bid: str,
    ask: str,
    bid_size: int = 100,
    ask_size: int = 100,
) -> MarketQuote:
    return MarketQuote(
        symbol=symbol,
        market=market,
        bid=Decimal(bid),
        ask=Decimal(ask),
        last=Decimal(bid),
        bid_size=bid_size,
        ask_size=ask_size,
    )


def test_detects_opportunity_for_same_symbol() -> None:
    quotes = [
        create_quote(
            symbol="GGAL",
            market="BYMA",
            bid="8190",
            ask="8200",
            ask_size=50,
        ),
        create_quote(
            symbol="GGAL",
            market="NYSE",
            bid="8350",
            ask="8360",
            bid_size=40,
        ),
    ]

    strategy = CrossMarketArbitrageStrategy()

    opportunities = strategy.detect(quotes)

    assert len(opportunities) == 1

    opportunity = opportunities[0]

    assert opportunity.symbol == "GGAL"
    assert opportunity.buy_market == "BYMA"
    assert opportunity.sell_market == "NYSE"
    assert opportunity.buy_price == Decimal("8200")
    assert opportunity.sell_price == Decimal("8350")
    assert opportunity.gross_spread == Decimal("150")
    assert opportunity.estimated_profit == Decimal("6000")


def test_does_not_compare_different_symbols() -> None:
    quotes = [
        create_quote(
            symbol="GGAL",
            market="BYMA",
            bid="8190",
            ask="8200",
        ),
        create_quote(
            symbol="YPFD",
            market="NYSE",
            bid="30000",
            ask="30100",
        ),
    ]

    strategy = CrossMarketArbitrageStrategy()

    assert strategy.detect(quotes) == []


def test_returns_empty_when_spread_is_not_positive() -> None:
    quotes = [
        create_quote(
            symbol="GGAL",
            market="BYMA",
            bid="8190",
            ask="8200",
        ),
        create_quote(
            symbol="GGAL",
            market="NYSE",
            bid="8180",
            ask="8190",
        ),
    ]

    strategy = CrossMarketArbitrageStrategy()

    assert strategy.detect(quotes) == []


def test_returns_empty_with_only_one_market() -> None:
    quotes = [
        create_quote(
            symbol="GGAL",
            market="BYMA",
            bid="8190",
            ask="8200",
        )
    ]

    strategy = CrossMarketArbitrageStrategy()

    assert strategy.detect(quotes) == []


def test_detects_opportunities_for_multiple_symbols() -> None:
    quotes = [
        create_quote("GGAL", "BYMA", "8190", "8200"),
        create_quote("GGAL", "NYSE", "8350", "8360"),
        create_quote("YPFD", "BYMA", "29900", "30000"),
        create_quote("YPFD", "NYSE", "30200", "30300"),
    ]

    strategy = CrossMarketArbitrageStrategy()

    opportunities = strategy.detect(quotes)

    assert len(opportunities) == 2
    assert {item.symbol for item in opportunities} == {
        "GGAL",
        "YPFD",
    }
