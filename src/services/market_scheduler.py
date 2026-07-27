from collections.abc import Callable
from time import sleep

from src.core.logger import get_logger
from src.services.market_pipeline import MarketPipeline

logger = get_logger(__name__)


class MarketScheduler:
    """Ejecuta el pipeline de mercado de forma periódica."""

    def __init__(
        self,
        pipeline: MarketPipeline,
        interval_seconds: float,
        max_runs: int | None = None,
        sleep_function: Callable[[float], None] = sleep,
    ) -> None:
        if interval_seconds <= 0:
            raise ValueError("El intervalo debe ser mayor que cero.")

        if max_runs is not None and max_runs <= 0:
            raise ValueError("max_runs debe ser mayor que cero.")

        self._pipeline = pipeline
        self._interval_seconds = interval_seconds
        self._max_runs = max_runs
        self._sleep_function = sleep_function

    def run(self) -> int:
        completed_runs = 0

        logger.info(
            "Scheduler iniciado. Intervalo: %s segundos.",
            self._interval_seconds,
        )

        while self._max_runs is None or completed_runs < self._max_runs:
            processed_quotes = self._pipeline.run()
            completed_runs += 1

            logger.info(
                "Ejecución %s completada. Cotizaciones procesadas: %s",
                completed_runs,
                processed_quotes,
            )

            if self._max_runs is not None and completed_runs >= self._max_runs:
                break

            self._sleep_function(self._interval_seconds)

        logger.info(
            "Scheduler finalizado. Ejecuciones completadas: %s",
            completed_runs,
        )

        return completed_runs
