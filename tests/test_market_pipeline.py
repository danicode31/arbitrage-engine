from pathlib import Path

from src.collectors.mock import MockCollector
from src.core.database import Database
from src.services.market_pipeline import MarketPipeline
from src.storage.market_quote_repository import MarketQuoteRepository


def test_market_pipeline_collects_and_saves_quotes(
    tmp_path: Path,
) -> None:
    database = Database(str(tmp_path / "test_arbitrage.db"))
    database.connect()
    database.initialize()

    repository = MarketQuoteRepository(database)
    collector = MockCollector()

    pipeline = MarketPipeline(
        collector=collector,
        repository=repository,
    )

    processed_quotes = pipeline.run()

    assert processed_quotes == 5
    assert repository.count() == 5
    assert collector.is_connected is False

    database.disconnect()
