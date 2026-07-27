from src.events.base import DomainEvent
from src.models.market import MarketQuote


class QuotesCollectedEvent(DomainEvent):
    """Se emite cuando finaliza una captura de cotizaciones."""

    quotes: list[MarketQuote]
