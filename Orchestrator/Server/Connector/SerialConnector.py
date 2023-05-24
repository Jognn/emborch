import asyncio
import logging
from asyncio import Queue
from typing import List, Coroutine

from serial.tools.list_ports_linux import comports

from Orchestrator.Server.Connector.Connector import Connector
from Orchestrator.Server.Connector.SerialPort import SerialPort


class SerialConnector(Connector):
    def __init__(self, message_queue: Queue):
        super().__init__(message_queue)
        serial_port_names = [comport.name for comport in comports() if "ACM" in comport.name]
        self.serial_ports = [SerialPort(name) for name in serial_port_names]

    def initialize(self, runners: List[Coroutine]) -> None:
        for port in self.serial_ports:
            runners.append(self._read_binary_message(port.name))

    def send_binary_message(self, node_id: int, binary_message: bytearray) -> None:
        # TODO: find by id :)
        self.serial_ports[0].write(binary_message)

    async def _read_binary_message(self, port_name: str) -> None:
        while True:
            serial_port = next(filter(lambda port: port.name == port_name, self.serial_ports))
            is_binary, line = await serial_port.read_bytes()

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
