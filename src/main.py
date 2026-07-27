from src.collectors.mock import MockCollector
from src.core.logger import get_logger

logger = get_logger(__name__)


def main() -> None:
    collector = MockCollector()

    try:
        collector.connect()
        quotes = collector.get_quotes()

        for quote in quotes:
            logger.info(
                "%s | Bid=%s Ask=%s Last=%s Spread=%s",
                quote.symbol,
                quote.bid,
                quote.ask,
                quote.last,
                quote.spread,
            )
    finally:
        collector.disconnect()


if __name__ == "__main__":
    main()
