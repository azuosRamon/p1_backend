import uuid
from datetime import datetime
from dataclasses import dataclass, field

@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_on: datetime = field(default_factory=datetime.now)

    def __str__(self):
        return f"[{self.__class__.__name__}] ID: {self.event_id} | Ocorrido em: {self.occurred_on}"
