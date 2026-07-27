from src.core.logger import get_logger
from src.events.market_events import QuotesCollectedEvent
from src.metrics.registry import MetricsRegistry
from src.services.arbitrage_engine import ArbitrageEngine

logger = get_logger(__name__)


class ArbitrageEventHandler:
    """Ejecuta el motor cuando se reciben nuevas cotizaciones."""

    def __init__(
        self,
        engine: ArbitrageEngine,
        registry: MetricsRegistry,
    ) -> None:
        self._engine = engine
        self._registry = registry

    def handle(
        self,
        event: QuotesCollectedEvent,
    ) -> None:
        opportunities = self._engine.analyze(event.quotes)

        self._registry.record_engine_run(opportunity_count=len(opportunities))

        logger.info(
            "Evento procesado. Oportunidades detectadas: %s",
            len(opportunities),
        )


class MetricsEventHandler:
    """Registra métricas cuando llegan nuevas cotizaciones."""

    def __init__(
        self,
        registry: MetricsRegistry,
    ) -> None:
        self._registry = registry

    def handle(
        self,
        event: QuotesCollectedEvent,
    ) -> None:
        self._registry.record_quotes_collected(quote_count=len(event.quotes))

        logger.info(
            "Métricas actualizadas. Cotizaciones recibidas: %s",
            len(event.quotes),
        )
