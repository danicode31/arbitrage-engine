from src.collectors.base import BaseCollector
from src.core.logger import get_logger
from src.storage.market_quote_repository import MarketQuoteRepository

logger = get_logger(__name__)


class MarketPipeline:
    """Coordina la captura y persistencia de cotizaciones."""

    def __init__(
        self,
        collector: BaseCollector,
        repository: MarketQuoteRepository,
    ) -> None:
        self._collector = collector
        self._repository = repository

    def run(self) -> int:
        logger.info("Iniciando pipeline de mercado.")

        try:
            self._collector.connect()

            quotes = self._collector.get_quotes()
            self._repository.save_many(quotes)

            total_quotes = len(quotes)

            logger.info(
                "Pipeline finalizado. Cotizaciones procesadas: %s",
                total_quotes,
            )

            return total_quotes
        except Exception:
            logger.exception("El pipeline de mercado terminó con error.")
            raise
        finally:
            self._collector.disconnect()
