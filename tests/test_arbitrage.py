from decimal import Decimal

from src.models.arbitrage import ArbitrageOpportunity


def test_profitable_opportunity() -> None:
    opportunity = ArbitrageOpportunity(
        symbol="ggal",
        buy_market="byma",
        sell_market="nyse",
        buy_price=Decimal("8200"),
        sell_price=Decimal("8350"),
        gross_spread=Decimal("150"),
        net_spread=Decimal("95"),
        estimated_profit=Decimal("9500"),
    )

    assert opportunity.is_profitable
    assert opportunity.symbol == "GGAL"
    assert opportunity.buy_market == "BYMA"
    assert opportunity.sell_market == "NYSE"


def test_non_profitable_opportunity() -> None:
    opportunity = ArbitrageOpportunity(
        symbol="GGAL",
        buy_market="BYMA",
        sell_market="NYSE",
        buy_price=Decimal("8200"),
        sell_price=Decimal("8210"),
        gross_spread=Decimal("10"),
        net_spread=Decimal("-15"),
        estimated_profit=Decimal("-1500"),
    )

    assert not opportunity.is_profitable
