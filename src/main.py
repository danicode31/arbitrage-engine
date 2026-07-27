from src.collectors.mock import MockCollector
from src.core.database import Database
from src.core.logger import get_logger
from src.events.event_bus import EventBus
from src.events.handlers import ArbitrageEventHandler
from src.events.market_events import QuotesCollectedEvent
from src.services.arbitrage_engine import ArbitrageEngine
from src.services.market_pipeline import MarketPipeline
from src.services.market_scheduler import MarketScheduler
from src.services.quote_services import QuoteService
from src.storage.market_quote_repository import MarketQuoteRepository
from src.strategies.cross_market import CrossMarketArbitrageStrategy

logger = get_logger(__name__)


def main() -> None:
    database = Database()

    try:
        database.connect()
        database.initialize()

        repository = MarketQuoteRepository(database)
        event_bus = EventBus()

        engine = ArbitrageEngine(strategies=[CrossMarketArbitrageStrategy()])

        arbitrage_handler = ArbitrageEventHandler(
            engine=engine,
        )

        event_bus.subscribe(
            QuotesCollectedEvent,
            arbitrage_handler.handle,
        )

        quote_service = QuoteService(
            collector=MockCollector(),
            repository=repository,
            event_bus=event_bus,
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
    finally:
        database.disconnect()


if __name__ == "__main__":
    main()
