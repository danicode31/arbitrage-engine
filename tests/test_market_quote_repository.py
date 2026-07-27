from decimal import Decimal
from pathlib import Path

from src.core.database import Database
from src.models.market import MarketQuote
from src.storage.market_quote_repository import MarketQuoteRepository


def test_repository_saves_quote(tmp_path: Path) -> None:
    database = Database(str(tmp_path / "test_arbitrage.db"))
    database.connect()
    database.initialize()

    repository = MarketQuoteRepository(database)

    quote = MarketQuote(
        symbol="GGAL",
        market="BYMA",
        bid=Decimal("8210"),
        ask=Decimal("8220"),
        last=Decimal("8215"),
        bid_size=Decimal("100"),
        ask_size=Decimal("150"),
    )

    repository.save(quote)

    assert repository.count() == 1

    database.disconnect()


def test_repository_saves_many_quotes(tmp_path: Path) -> None:
    database = Database(str(tmp_path / "test_arbitrage.db"))
    database.connect()
    database.initialize()

    repository = MarketQuoteRepository(database)

    quotes = [
        MarketQuote(
            symbol="GGAL",
            market="BYMA",
            bid=Decimal("8210"),
            ask=Decimal("8220"),
            last=Decimal("8215"),
        ),
        MarketQuote(
            symbol="YPFD",
            market="BYMA",
            bid=Decimal("47000"),
            ask=Decimal("47010"),
            last=Decimal("47005"),
        ),
    ]

    repository.save_many(quotes)

    assert repository.count() == 2

    database.disconnect()
