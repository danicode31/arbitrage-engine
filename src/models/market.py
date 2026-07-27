from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class MarketQuote(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    market: str = Field(min_length=1, max_length=20)

    bid: Decimal = Field(ge=0)
    ask: Decimal = Field(ge=0)
    last: Decimal = Field(ge=0)

    bid_size: Decimal = Field(default=Decimal("0"), ge=0)
    ask_size: Decimal = Field(default=Decimal("0"), ge=0)

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("symbol", "market")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("ask")
    @classmethod
    def validate_ask(cls, ask: Decimal, info) -> Decimal:
        bid = info.data.get("bid")

        if bid is not None and ask < bid:
            raise ValueError("El precio ask no puede ser menor que el bid")

        return ask

    @property
    def spread(self) -> Decimal:
        return self.ask - self.bid

    @property
    def mid_price(self) -> Decimal:
        return (self.bid + self.ask) / Decimal("2")

    @property
    def spread_percentage(self) -> Decimal:
        if self.mid_price == 0:
            return Decimal("0")

        return (self.spread / self.mid_price) * Decimal("100")
