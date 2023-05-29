import dataclasses
from typing import Optional


@dataclasses.dataclass
class Node:
    node_id: int
    available_memory_bytes: int
    supported_features: int
    running_script: Optional[str] = None
