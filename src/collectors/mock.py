from decimal import Decimal
from random import randint
from typing import ClassVar

from src.collectors.base import BaseCollector
from src.core.logger import get_logger
from src.models.market import MarketQuote

logger = get_logger(__name__)


class MockCollector(BaseCollector):
    """Collector que genera cotizaciones simuladas para varios activos."""

    BASE_PRICES: ClassVar[dict[str, Decimal]] = {
        "GGAL": Decimal("8200"),
        "YPFD": Decimal("47000"),
        "PAMP": Decimal("4100"),
        "TXAR": Decimal("900"),
        "AL30": Decimal("75000"),
    }

    def __init__(self) -> None:
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

    def connect(self) -> None:
        if self._connected:
            logger.warning("MockCollector ya estaba conectado.")
            return

        self._connected = True
        logger.info("MockCollector conectado.")

    def disconnect(self) -> None:
        if not self._connected:
            logger.warning("MockCollector ya estaba desconectado.")
            return

        self._connected = False
        logger.info("MockCollector desconectado.")

    def get_quotes(self) -> list[MarketQuote]:
        if not self._connected:
            raise RuntimeError(
                "El collector debe estar conectado antes de obtener cotizaciones."
            )

        quotes: list[MarketQuote] = []

        for symbol, base_price in self.BASE_PRICES.items():
            variation = Decimal(randint(-20, 20))
            bid = base_price + variation
            ask = bid + Decimal("1")

            quotes.append(
                MarketQuote(
                    symbol=symbol,
                    market="BYMA",
                    bid=bid,
                    ask=ask,
                    last=bid,
                    bid_size=Decimal("100"),
                    ask_size=Decimal("120"),
                )
            )

        logger.info("Se generaron %s cotizaciones simuladas.", len(quotes))

        return quotes
