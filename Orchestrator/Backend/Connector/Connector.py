import asyncio
import logging
from asyncio import Queue
from typing import Dict, List, Coroutine, TypeVar

from Orchestrator.Backend.Connector.PhysicalConnector import PhysicalConnector
from Orchestrator.Backend.MessageService.Message import Message


class Connector:
    M = TypeVar('M', bound=Message)

    def __init__(self, physical_connector: PhysicalConnector, message_queue: Queue) -> None:
        self.physical_connector: PhysicalConnector = physical_connector
        self.message_queue = message_queue
        self.port_names = self.physical_connector.get_port_names()
        self.port_node_map: Dict[int, str] = dict()

    def start_ports(self, runners: List[Coroutine]) -> None:
        for port_name in self.port_names:
            runners.append(self.read_binary_message(port_name))

    def send_binary_message(self, node_id: int, binary_message: bytearray) -> None:
        port_name = self.port_names[0]
        self.physical_connector.send_message(port_name, binary_message)

    async def read_binary_message(self, port_name: str) -> None:
        while True:
            is_binary, line = await self.physical_connector.read_message(port_name)

            if line:
                message_type_name = 'Binary' if is_binary else 'Text'
                logging.info(
                    f"{message_type_name} message from {port_name}"
                    f" -> {line if is_binary else line[:-1].decode('ISO-8859-1')}")

                if is_binary:
                    # TODO: Handle the 'Full' exception?
                    self.message_queue.put_nowait(line)
                await asyncio.sleep(0.5)
            else:
                await asyncio.sleep(3)
