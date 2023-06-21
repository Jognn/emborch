from typing import Optional, Any


class EventComponent:
    def __init__(self):
        self.event_bus: Optional[Any] = None

    def set_event_bus(self, event_bus: Any) -> None:
        self.event_bus = event_bus
