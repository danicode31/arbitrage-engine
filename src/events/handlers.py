from src.core.logger import get_logger
from src.events.market_events import QuotesCollectedEvent
from src.services.arbitrage_engine import ArbitrageEngine

logger = get_logger(__name__)


class ArbitrageEventHandler:
    """Ejecuta el motor cuando se reciben nuevas cotizaciones."""

    def __init__(
        self,
        engine: ArbitrageEngine,
    ) -> None:
        self._engine = engine

    def handle(
        self,
        event: QuotesCollectedEvent,
    ) -> None:
        opportunities = self._engine.analyze(event.quotes)

        logger.info(
            "Evento procesado. Oportunidades detectadas: %s",
            len(opportunities),
        )
