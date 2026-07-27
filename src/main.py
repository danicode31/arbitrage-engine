from src.collectors.mock import MockCollector
from src.core.database import Database
from src.core.logger import get_logger
from src.services.market_pipeline import MarketPipeline
from src.storage.market_quote_repository import MarketQuoteRepository

logger = get_logger(__name__)


def main() -> None:
    database = Database()

    try:
        database.connect()
        database.initialize()

        repository = MarketQuoteRepository(database)
        collector = MockCollector()

        pipeline = MarketPipeline(
            collector=collector,
            repository=repository,
        )

        processed_quotes = pipeline.run()

        logger.info(
            "Total histórico de cotizaciones: %s",
            repository.count(),
        )
        logger.info(
            "Cotizaciones procesadas en esta ejecución: %s",
            processed_quotes,
        )
    finally:
        database.disconnect()


if __name__ == "__main__":
    main()
