import dataclasses
from enum import Enum


class EventType(Enum):
    NOT_SET = -1
    NODE_REGISTER = 0
    REQUEST_SEND_SCRIPT = 1
    SEND_SCRIPT = 2
    MONITOR_NODE = 3
    MONITOR_NODE_RESULT = 4
    ALTER_NODE_STATE = 5


@dataclasses.dataclass
class Event:
    def __init__(self, event_type: EventType = EventType.NOT_SET):
        self.event_type = event_type
