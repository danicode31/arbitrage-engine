from decimal import Decimal

from src.core.config import settings
from src.core.logger import get_logger
from src.models.market import MarketQuote


logger = get_logger(__name__)


def main() -> None:
    logger.info("Iniciando %s", settings.project_name)

    quote = MarketQuote(
        symbol="GGAL",
        market="BYMA",
        bid=Decimal("8210"),
        ask=Decimal("8220"),
        last=Decimal("8215"),
        bid_size=Decimal("100"),
        ask_size=Decimal("150"),
    )

    logger.info(
        "Cotización %s | Bid: %s | Ask: %s | Spread: %.4f%%",
        quote.symbol,
        quote.bid,
        quote.ask,
        quote.spread_percentage,
    )


if __name__ == "__main__":
    main()
