from src.collectors.mock import MockCollector
from src.core.database import Database
from src.core.logger import get_logger
from src.storage.market_quote_repository import MarketQuoteRepository

logger = get_logger(__name__)


def main() -> None:
    collector = MockCollector()
    database = Database()

    try:
        database.connect()
        database.initialize()

        collector.connect()
        quotes = collector.get_quotes()

        repository = MarketQuoteRepository(database)
        repository.save_many(quotes)

        logger.info(
            "Total de cotizaciones guardadas: %s",
            repository.count(),
        )
    finally:
        collector.disconnect()
        database.disconnect()


if __name__ == "__main__":
    main()
