from abc import abstractmethod, ABC
from typing import List


class PhysicalConnector(ABC):

    @abstractmethod
    async def read_message(self, port_name: str):
        pass

    @abstractmethod
    def send_message(self, port_name: str, binary_message: bytearray):
        pass

    @abstractmethod
    def get_port_names(self) -> List[str]:
        pass
