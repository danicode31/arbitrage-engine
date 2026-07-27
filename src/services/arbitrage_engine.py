from src.core.logger import get_logger
from src.models.arbitrage import ArbitrageOpportunity
from src.models.market import MarketQuote
from src.strategies.base import BaseStrategy

logger = get_logger(__name__)


class ArbitrageEngine:
    """Ejecuta estrategias de arbitraje sobre cotizaciones."""

    def __init__(
        self,
        strategies: list[BaseStrategy],
    ) -> None:
        self._strategies = strategies

    def analyze(
        self,
        quotes: list[MarketQuote],
    ) -> list[ArbitrageOpportunity]:
        opportunities: list[ArbitrageOpportunity] = []

        for strategy in self._strategies:
            detected = strategy.detect(quotes)
            opportunities.extend(detected)

            logger.info(
                "Estrategia %s detectó %s oportunidades.",
                strategy.__class__.__name__,
                len(detected),
            )

        return opportunities
