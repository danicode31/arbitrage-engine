from src.collectors.mock import MockCollector
from src.core.database import Database
from src.core.logger import get_logger
from src.services.market_pipeline import MarketPipeline
from src.services.market_scheduler import MarketScheduler
from src.services.quote_services import QuoteService
from src.storage.market_quote_repository import MarketQuoteRepository

logger = get_logger(__name__)


def main() -> None:
    database = Database()

    try:
        database.connect()
        database.initialize()

        repository = MarketQuoteRepository(database)

        quote_service = QuoteService(
            collector=MockCollector(),
            repository=repository,
        )

        pipeline = MarketPipeline(
            quote_service=quote_service,
        )

        scheduler = MarketScheduler(
            pipeline=pipeline,
            interval_seconds=5,
            max_runs=3,
        )

        completed_runs = scheduler.run()

        logger.info(
            "Ejecuciones completadas: %s",
            completed_runs,
        )
        logger.info(
            "Total histórico de cotizaciones: %s",
            repository.count(),
        )
        logger.info(
            "Últimas cotizaciones disponibles: %s",
            len(quote_service.latest_quotes()),
        )
    finally:
        database.disconnect()


if __name__ == "__main__":
    main()
