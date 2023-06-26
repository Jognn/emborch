import asyncio
import dataclasses
from enum import Enum
from typing import Optional


class NodeState(Enum):
    Connected = "Connected"
    Working = "Working"
    Disconnected = "Disconnected"
    NotInitialized = "Not initialized"
    Error = "Error"


@dataclasses.dataclass
class Node:
    node_id: int
    name: str
    initial_memory_bytes: int
    supported_features: int
    state: NodeState = NodeState.NotInitialized
    running_script: Optional[str] = None
    status_queue: asyncio.Queue = asyncio.Queue(maxsize=1)

    def __post_init__(self):
        self.available_memory_bytes = self.initial_memory_bytes
