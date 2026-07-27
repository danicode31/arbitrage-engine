from src.collectors.mock import MockCollector
from src.core.database import Database
from src.core.logger import get_logger
from src.events.event_bus import EventBus
from src.events.handlers import (
    ArbitrageEventHandler,
    MetricsEventHandler,
)
from src.events.market_events import QuotesCollectedEvent
from src.metrics.registry import MetricsRegistry
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

        # Infraestructura
        repository = MarketQuoteRepository(database)
        event_bus = EventBus()
        metrics_registry = MetricsRegistry()

        # Collector
        collector = MockCollector()

        # Servicios
        quote_service = QuoteService(
            collector=collector,
            repository=repository,
            event_bus=event_bus,
        )

        # Motor de arbitraje
        engine = ArbitrageEngine(
            strategies=[
                CrossMarketArbitrageStrategy(),
            ]
        )

        # Handlers
        arbitrage_handler = ArbitrageEventHandler(
            engine=engine,
            registry=metrics_registry,
        )

        metrics_handler = MetricsEventHandler(
            registry=metrics_registry,
        )

        # Suscripciones
        event_bus.subscribe(
            QuotesCollectedEvent,
            arbitrage_handler.handle,
        )

        event_bus.subscribe(
            QuotesCollectedEvent,
            metrics_handler.handle,
        )

        # Pipeline
        pipeline = MarketPipeline(
            quote_service=quote_service,
        )

        # Scheduler
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
            "Métricas: %s",
            metrics_registry.snapshot(),
        )

    finally:
        database.disconnect()


if __name__ == "__main__":
    main()
