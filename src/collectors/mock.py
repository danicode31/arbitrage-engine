from decimal import Decimal
from random import randint

from src.collectors.base import BaseCollector
from src.models.market import MarketQuote


class MockCollector(BaseCollector):
    """Collector que genera cotizaciones simuladas para varios activos."""

    BASE_PRICES: dict[str, Decimal] = {
        "GGAL": Decimal("8200"),
        "YPFD": Decimal("47000"),
        "PAMP": Decimal("4100"),
        "TXAR": Decimal("900"),
        "AL30": Decimal("75000"),
    }

    def connect(self) -> None:
        print("MockCollector conectado.")

    def disconnect(self) -> None:
        print("MockCollector desconectado.")

    def get_quotes(self) -> list[MarketQuote]:
        quotes: list[MarketQuote] = []

        for symbol, base_price in self.BASE_PRICES.items():
            variation = Decimal(randint(-20, 20))
            bid = base_price + variation
            ask = bid + Decimal("1")

            quote = MarketQuote(
                symbol=symbol,
                market="BYMA",
                bid=bid,
                ask=ask,
                last=bid,
                bid_size=Decimal("100"),
                ask_size=Decimal("120"),
            )

            quotes.append(quote)

        return quotes
