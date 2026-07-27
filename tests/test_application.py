from pathlib import Path

from src.application.app import ArbitrageApplication
from src.core.database import Database
from src.storage.market_quote_repository import (
    MarketQuoteRepository,
)


def test_application_runs_configured_iterations(
    tmp_path: Path,
) -> None:
    database = Database(str(tmp_path / "application_test.db"))

    application = ArbitrageApplication(
        interval_seconds=0.001,
        max_runs=2,
        database=database,
    )

    completed_runs = application.run()

    assert completed_runs == 2


def test_application_collects_metrics(
    tmp_path: Path,
) -> None:
    database = Database(str(tmp_path / "metrics_test.db"))

    application = ArbitrageApplication(
        interval_seconds=0.001,
        max_runs=2,
        database=database,
    )

    application.run()

    metrics = application.metrics_snapshot()

    assert metrics["quote_events"] == 2
    assert metrics["quotes_collected"] == 10
    assert metrics["engine_runs"] == 2


def test_application_can_run_multiple_times(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "multiple_runs.db"

    first_application = ArbitrageApplication(
        interval_seconds=0.001,
        max_runs=1,
        database=Database(str(database_path)),
    )

    second_application = ArbitrageApplication(
        interval_seconds=0.001,
        max_runs=1,
        database=Database(str(database_path)),
    )

    first_result = first_application.run()
    second_result = second_application.run()

    assert first_result == 1
    assert second_result == 1


def test_application_persists_quotes_between_runs(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "persistent.db"

    first_application = ArbitrageApplication(
        interval_seconds=0.001,
        max_runs=1,
        database=Database(str(database_path)),
    )

    second_application = ArbitrageApplication(
        interval_seconds=0.001,
        max_runs=1,
        database=Database(str(database_path)),
    )

    first_application.run()
    second_application.run()

    verification_database = Database(str(database_path))
    verification_database.connect()
    verification_database.initialize()

    try:
        repository = MarketQuoteRepository(verification_database)

        assert repository.count() == 10
    finally:
        verification_database.disconnect()
