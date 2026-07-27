from abc import ABC, abstractmethod

from src.models.arbitrage import ArbitrageOpportunity
from src.models.market import MarketQuote


class BaseStrategy(ABC):
    """Contrato común para las estrategias de arbitraje."""

    @abstractmethod
    def detect(
        self,
        quotes: list[MarketQuote],
    ) -> list[ArbitrageOpportunity]:
        """Detecta oportunidades a partir de cotizaciones."""
