from datetime import UTC, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class ArbitrageOpportunity(BaseModel):
    """Representa una oportunidad de arbitraje detectada."""

    symbol: str
    buy_market: str
    sell_market: str

    buy_price: Decimal
    sell_price: Decimal

    gross_spread: Decimal
    net_spread: Decimal
    estimated_profit: Decimal

    detected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @field_validator(
        "symbol",
        "buy_market",
        "sell_market",
        mode="before",
    )
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return value.strip().upper()

    @property
    def is_profitable(self) -> bool:
        return self.net_spread > Decimal("0")
