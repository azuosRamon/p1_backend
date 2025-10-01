from typing import Callable, Dict, List, Type
from shared.domain_event import DomainEvent

class EventDispatcher:
    def __init__(self):
        self._handlers: Dict[Type[DomainEvent], List[Callable[[DomainEvent], None]]] = {}

    def register_handler(self, event_type: Type[DomainEvent], handler: Callable[[DomainEvent], None]) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def dispatch(self, event: DomainEvent) -> None:
        handlers = self._handlers.get(type(event), [])
        for handler in handlers:
            handler(event)

dispatcher = EventDispatcher()
