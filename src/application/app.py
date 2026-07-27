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


class ArbitrageApplication:
    """Configura, ejecuta y libera los recursos de la aplicación."""

    def __init__(
        self,
        interval_seconds: float = 5,
        max_runs: int | None = 3,
        database: Database | None = None,
    ) -> None:
        self._interval_seconds = interval_seconds
        self._max_runs = max_runs

        self._database = database
        self._repository: MarketQuoteRepository | None = None
        self._metrics_registry: MetricsRegistry | None = None
        self._scheduler: MarketScheduler | None = None

    def setup(self) -> None:
        """Construye y conecta todos los componentes de la aplicación."""

        logger.info("Configurando aplicación de arbitraje.")

        database = self._database or Database()
        database.connect()
        database.initialize()

        repository = MarketQuoteRepository(database)
        event_bus = EventBus()
        metrics_registry = MetricsRegistry()

        collector = MockCollector()

        quote_service = QuoteService(
            collector=collector,
            repository=repository,
            event_bus=event_bus,
        )

        engine = ArbitrageEngine(
            strategies=[
                CrossMarketArbitrageStrategy(),
            ]
        )

        arbitrage_handler = ArbitrageEventHandler(
            engine=engine,
            registry=metrics_registry,
        )

        metrics_handler = MetricsEventHandler(
            registry=metrics_registry,
        )

        event_bus.subscribe(
            QuotesCollectedEvent,
            arbitrage_handler.handle,
        )

        event_bus.subscribe(
            QuotesCollectedEvent,
            metrics_handler.handle,
        )

        pipeline = MarketPipeline(
            quote_service=quote_service,
        )

        scheduler = MarketScheduler(
            pipeline=pipeline,
            interval_seconds=self._interval_seconds,
            max_runs=self._max_runs,
        )

        self._database = database
        self._repository = repository
        self._metrics_registry = metrics_registry
        self._scheduler = scheduler

        logger.info("Aplicación configurada correctamente.")

    def run(self) -> int:
        """Ejecuta la aplicación y devuelve las corridas completadas."""

        try:
            self.setup()

            scheduler = self._require_scheduler()
            completed_runs = scheduler.run()

            self._log_final_state(
                completed_runs=completed_runs,
            )

            return completed_runs
        finally:
            self.shutdown()

    def shutdown(self) -> None:
        """Libera los recursos abiertos por la aplicación."""

        if self._database is not None:
            self._database.disconnect()
            self._database = None

            logger.info("Base de datos desconectada.")

    def metrics_snapshot(
        self,
    ) -> dict[str, object]:
        """Devuelve una copia de las métricas actuales."""

        if self._metrics_registry is None:
            return {}

        return dict(self._metrics_registry.snapshot())

    def _require_scheduler(self) -> MarketScheduler:
        if self._scheduler is None:
            raise RuntimeError("La aplicación no fue configurada correctamente.")

        return self._scheduler

    def _log_final_state(
        self,
        completed_runs: int,
    ) -> None:
        logger.info(
            "Ejecuciones completadas: %s",
            completed_runs,
        )

        if self._repository is not None:
            logger.info(
                "Total histórico de cotizaciones: %s",
                self._repository.count(),
            )

        if self._metrics_registry is not None:
            logger.info(
                "Métricas finales: %s",
                self._metrics_registry.snapshot(),
            )
