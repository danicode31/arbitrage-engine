from decimal import Decimal

from src.events.event_bus import EventBus
from src.events.market_events import QuotesCollectedEvent
from src.models.market import MarketQuote


def create_quote() -> MarketQuote:
    return MarketQuote(
        symbol="GGAL",
        market="BYMA",
        bid=Decimal("8190"),
        ask=Decimal("8200"),
        last=Decimal("8195"),
        bid_size=100,
        ask_size=100,
    )


def test_event_bus_publishes_event_to_subscriber() -> None:
    event_bus = EventBus()
    received_events: list[QuotesCollectedEvent] = []

    def handler(event: QuotesCollectedEvent) -> None:
        received_events.append(event)

    event_bus.subscribe(
        QuotesCollectedEvent,
        handler,
    )

    event = QuotesCollectedEvent(
        quotes=[create_quote()],
    )

    handled_count = event_bus.publish(event)

    assert handled_count == 1
    assert received_events == [event]


def test_event_bus_supports_multiple_subscribers() -> None:
    event_bus = EventBus()
    calls: list[str] = []

    def first_handler(event: QuotesCollectedEvent) -> None:
        calls.append("first")

    def second_handler(event: QuotesCollectedEvent) -> None:
        calls.append("second")

    event_bus.subscribe(
        QuotesCollectedEvent,
        first_handler,
    )
    event_bus.subscribe(
        QuotesCollectedEvent,
        second_handler,
    )

    event_bus.publish(
        QuotesCollectedEvent(
            quotes=[create_quote()],
        )
    )

    assert calls == ["first", "second"]


def test_event_bus_returns_zero_without_subscribers() -> None:
    event_bus = EventBus()

    handled_count = event_bus.publish(
        QuotesCollectedEvent(
            quotes=[create_quote()],
        )
    )

    assert handled_count == 0
