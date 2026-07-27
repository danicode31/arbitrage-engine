from src.application.app import ArbitrageApplication
from src.core.logger import get_logger

logger = get_logger(__name__)


def main() -> None:
    logger.info("Iniciando Arbitrage Engine.")

    application = ArbitrageApplication(
        interval_seconds=5,
        max_runs=3,
    )

    application.run()

    logger.info("Arbitrage Engine finalizado.")


if __name__ == "__main__":
    main()
