from collections import defaultdict
from decimal import Decimal

from src.models.arbitrage import ArbitrageOpportunity
from src.models.market import MarketQuote
from src.strategies.base import BaseStrategy


class CrossMarketArbitrageStrategy(BaseStrategy):
    """Detecta diferencias de precio del mismo símbolo entre mercados."""

    def detect(
        self,
        quotes: list[MarketQuote],
    ) -> list[ArbitrageOpportunity]:
        quotes_by_symbol = self._group_by_symbol(quotes)
        opportunities: list[ArbitrageOpportunity] = []

        for symbol, symbol_quotes in quotes_by_symbol.items():
            opportunity = self._find_best_opportunity(
                symbol=symbol,
                quotes=symbol_quotes,
            )

            if opportunity is not None:
                opportunities.append(opportunity)

        return opportunities

    @staticmethod
    def _group_by_symbol(
        quotes: list[MarketQuote],
    ) -> dict[str, list[MarketQuote]]:
        grouped_quotes: defaultdict[str, list[MarketQuote]] = defaultdict(list)

        for quote in quotes:
            grouped_quotes[quote.symbol].append(quote)

        return dict(grouped_quotes)

    @staticmethod
    def _find_best_opportunity(
        symbol: str,
        quotes: list[MarketQuote],
    ) -> ArbitrageOpportunity | None:
        if len(quotes) < 2:
            return None

        best_buy_quote = min(
            quotes,
            key=lambda quote: quote.ask,
        )

        sell_candidates = [
            quote for quote in quotes if quote.market != best_buy_quote.market
        ]

        if not sell_candidates:
            return None

        best_sell_quote = max(
            sell_candidates,
            key=lambda quote: quote.bid,
        )

        gross_spread = best_sell_quote.bid - best_buy_quote.ask

        if gross_spread <= Decimal("0"):
            return None

        available_quantity = min(
            best_buy_quote.ask_size,
            best_sell_quote.bid_size,
        )

        estimated_profit = gross_spread * Decimal(str(available_quantity))

        return ArbitrageOpportunity(
            symbol=symbol,
            buy_market=best_buy_quote.market,
            sell_market=best_sell_quote.market,
            buy_price=best_buy_quote.ask,
            sell_price=best_sell_quote.bid,
            gross_spread=gross_spread,
            net_spread=gross_spread,
            estimated_profit=estimated_profit,
        )
