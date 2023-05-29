import dataclasses
from typing import Optional


@dataclasses.dataclass
class Node:
    def __init__(self, available_memory: int, supported_features: int):
        self.node_id: int = 0
        self.available_memory: int = available_memory
        self.supported_features: int = supported_features
        self.running_script: Optional[str] = None
