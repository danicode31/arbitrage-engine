from decimal import Decimal

from src.models.arbitrage import ArbitrageOpportunity
from src.models.market import MarketQuote
from src.strategies.base import BaseStrategy


class DummyArbitrageStrategy(BaseStrategy):
    """Estrategia temporal para validar el flujo del motor."""

    def detect(
        self,
        quotes: list[MarketQuote],
    ) -> list[ArbitrageOpportunity]:
        if len(quotes) < 2:
            return []

        buy_quote = min(quotes, key=lambda quote: quote.ask)
        sell_quote = max(quotes, key=lambda quote: quote.bid)

        gross_spread = sell_quote.bid - buy_quote.ask

        if gross_spread <= Decimal("0"):
            return []

        return [
            ArbitrageOpportunity(
                symbol=buy_quote.symbol,
                buy_market=buy_quote.market,
                sell_market=sell_quote.market,
                buy_price=buy_quote.ask,
                sell_price=sell_quote.bid,
                gross_spread=gross_spread,
                net_spread=gross_spread,
                estimated_profit=gross_spread,
            )
        ]
