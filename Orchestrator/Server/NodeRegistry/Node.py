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
    status_queue: asyncio.Queue
    state: NodeState = NodeState.NotInitialized
    running_script: Optional[str] = None

    def __post_init__(self):
        self.available_memory_bytes = self.initial_memory_bytes
