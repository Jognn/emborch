from abc import abstractmethod, ABC
from asyncio import Queue
from typing import Dict, TypeVar, Coroutine, List

from Orchestrator.Backend.MessageService.Message import Message


class Connector(ABC):
    M = TypeVar('M', bound=Message)

    def __init__(self, message_queue: Queue) -> None:
        self.message_queue = message_queue
        self.port_node_map: Dict[int, str] = dict()

    @abstractmethod
    def initialize(self, runners: List[Coroutine]) -> None:
        pass

    @abstractmethod
    def send_binary_message(self, node_id: int, binary_message: bytearray) -> None:
        pass
