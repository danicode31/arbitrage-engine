from collections.abc import Sequence

from src.core.database import Database
from src.core.logger import get_logger
from src.models.market import MarketQuote

logger = get_logger(__name__)


class MarketQuoteRepository:
    """Gestiona la persistencia de cotizaciones en DuckDB."""

    def __init__(self, database: Database) -> None:
        self._database = database

    def save(self, quote: MarketQuote) -> None:
        self._database.connection.execute(
            """
            INSERT INTO market_quotes (
                symbol,
                market,
                bid,
                ask,
                last,
                bid_size,
                ask_size,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                quote.symbol,
                quote.market,
                quote.bid,
                quote.ask,
                quote.last,
                quote.bid_size,
                quote.ask_size,
                quote.timestamp,
            ],
        )

        logger.info(
            "Cotización guardada: %s %s",
            quote.market,
            quote.symbol,
        )

    def save_many(self, quotes: Sequence[MarketQuote]) -> None:
        if not quotes:
            logger.warning("No se recibieron cotizaciones para guardar.")
            return

        rows = [
            (
                quote.symbol,
                quote.market,
                quote.bid,
                quote.ask,
                quote.last,
                quote.bid_size,
                quote.ask_size,
                quote.timestamp,
            )
            for quote in quotes
        ]

        self._database.connection.executemany(
            """
            INSERT INTO market_quotes (
                symbol,
                market,
                bid,
                ask,
                last,
                bid_size,
                ask_size,
                timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

        logger.info(
            "Se guardaron %s cotizaciones.",
            len(quotes),
        )

    def count(self) -> int:
        result = self._database.connection.execute(
            "SELECT COUNT(*) FROM market_quotes"
        ).fetchone()

        if result is None:
            return 0

        return int(result[0])
