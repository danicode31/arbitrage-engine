from src.collectors.base import BaseCollector
from src.core.logger import get_logger
from src.events.event_bus import EventBus
from src.events.market_events import QuotesCollectedEvent
from src.models.market import MarketQuote
from src.storage.market_quote_repository import MarketQuoteRepository

logger = get_logger(__name__)


class QuoteService:
    """Centraliza la captura, persistencia y acceso a cotizaciones."""

    def __init__(
        self,
        collector: BaseCollector,
        repository: MarketQuoteRepository,
        event_bus: EventBus,
    ) -> None:
        self._collector = collector
        self._repository = repository
        self._event_bus = event_bus
        self._latest_quotes: list[MarketQuote] = []

    def collect(self) -> list[MarketQuote]:
        logger.info("Iniciando captura de cotizaciones.")

        try:
            self._collector.connect()

            quotes = self._collector.get_quotes()

            self._repository.save_many(quotes)
            self._latest_quotes = list(quotes)

            event = QuotesCollectedEvent(
                quotes=list(quotes),
            )
            self._event_bus.publish(event)

            logger.info(
                "Cotizaciones capturadas y persistidas: %s",
                len(quotes),
            )

            return list(quotes)
        except Exception:
            logger.exception("Error durante la captura de cotizaciones.")
            raise
        finally:
            self._collector.disconnect()

    def latest_quotes(self) -> list[MarketQuote]:
        return list(self._latest_quotes)
