from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.models.market import MarketQuote


def test_market_quote_creation() -> None:
    quote = MarketQuote(
        symbol="ggal",
        market="byma",
        bid=Decimal("8210"),
        ask=Decimal("8220"),
        last=Decimal("8215"),
        bid_size=Decimal("100"),
        ask_size=Decimal("150"),
    )

    assert quote.symbol == "GGAL"
    assert quote.market == "BYMA"
    assert quote.spread == Decimal("10")
    assert quote.mid_price == Decimal("8215")


def test_ask_cannot_be_lower_than_bid() -> None:
    with pytest.raises(ValidationError):
        MarketQuote(
            symbol="GGAL",
            market="BYMA",
            bid=Decimal("8220"),
            ask=Decimal("8210"),
            last=Decimal("8215"),
        )
