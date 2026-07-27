from collections import defaultdict
from collections.abc import Callable
from typing import Any, TypeVar

from src.core.logger import get_logger
from src.events.base import DomainEvent

logger = get_logger(__name__)

EventType = TypeVar("EventType", bound=DomainEvent)
EventHandler = Callable[[Any], None]


class EventBus:
    """Event bus interno, síncrono y en memoria."""

    def __init__(self) -> None:
        self._subscribers: defaultdict[
            type[DomainEvent],
            list[EventHandler],
        ] = defaultdict(list)

    def subscribe(
        self,
        event_type: type[EventType],
        handler: Callable[[EventType], None],
    ) -> None:
        self._subscribers[event_type].append(handler)

        logger.info(
            "Handler %s suscripto a %s.",
            handler.__name__,
            event_type.__name__,
        )

    def publish(
        self,
        event: DomainEvent,
    ) -> int:
        handlers = self._subscribers[type(event)]

        logger.info(
            "Publicando evento %s a %s handlers.",
            type(event).__name__,
            len(handlers),
        )

        for handler in handlers:
            handler(event)

        return len(handlers)
