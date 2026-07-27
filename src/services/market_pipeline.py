from src.core.logger import get_logger
from src.services.quote_services import QuoteService

logger = get_logger(__name__)


class MarketPipeline:
    """Coordina una ejecución del flujo de cotizaciones."""

    def __init__(
        self,
        quote_service: QuoteService,
    ) -> None:
        self._quote_service = quote_service

    def run(self) -> int:
        logger.info("Iniciando pipeline de mercado.")

        quotes = self._quote_service.collect()
        processed_quotes = len(quotes)

        logger.info(
            "Pipeline finalizado. Cotizaciones procesadas: %s",
            processed_quotes,
        )

        return processed_quotes
