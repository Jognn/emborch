import dataclasses
from typing import Optional


@dataclasses.dataclass
class Node:
    node_id: int
    name: str
    available_memory_bytes: int
    supported_features: int
    is_alive: bool = True
    running_script: Optional[str] = None
