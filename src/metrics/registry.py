from datetime import UTC, datetime
from threading import Lock


class MetricsRegistry:
    """Registro interno y thread-safe de métricas del sistema."""

    def __init__(self) -> None:
        self._lock = Lock()

        self._quote_events = 0
        self._quotes_collected = 0
        self._engine_runs = 0
        self._opportunities_detected = 0
        self._last_updated_at: datetime | None = None

    def record_quotes_collected(
        self,
        quote_count: int,
    ) -> None:
        if quote_count < 0:
            raise ValueError("quote_count no puede ser negativo.")

        with self._lock:
            self._quote_events += 1
            self._quotes_collected += quote_count
            self._touch()

    def record_engine_run(
        self,
        opportunity_count: int,
    ) -> None:
        if opportunity_count < 0:
            raise ValueError("opportunity_count no puede ser negativo.")

        with self._lock:
            self._engine_runs += 1
            self._opportunities_detected += opportunity_count
            self._touch()

    def snapshot(self) -> dict[str, int | datetime | None]:
        """Devuelve una copia inmutable del estado actual."""

        with self._lock:
            return {
                "quote_events": self._quote_events,
                "quotes_collected": self._quotes_collected,
                "engine_runs": self._engine_runs,
                "opportunities_detected": (self._opportunities_detected),
                "last_updated_at": self._last_updated_at,
            }

    def _touch(self) -> None:
        self._last_updated_at = datetime.now(UTC)
