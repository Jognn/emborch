import asyncio
import logging
from asyncio import Queue
from typing import List, Optional

from serial.tools.list_ports_linux import comports

from Orchestrator.AsyncTaskManager import AsyncTaskManager
from Orchestrator.Server.Connector.Connector import Connector
from Orchestrator.Server.Connector.SerialPort import SerialPort


class SerialConnector(Connector):
    def __init__(self, async_task_manager: AsyncTaskManager, message_queue: Queue):
        super().__init__(message_queue)
        serial_port_names = [comport.name for comport in comports() if "ACM" in comport.name]
        self.serial_ports = [SerialPort(name) for name in serial_port_names]
        self.ports_waiting: List[SerialPort] = []
        self.async_task_manager = async_task_manager

        for port in self.serial_ports:
            self.async_task_manager.add_task(self._read_binary_message(port))

    def send_binary_message(self, node_id: int, binary_message: bytearray) -> None:
        port: Optional[SerialPort] = next(filter(lambda x: x.node_id == node_id, self.serial_ports), None)

        if port is not None:
            logging.debug(f"[Connector] Sending {binary_message}")
            write_result = port.write(binary_message)
            if write_result is None:
                logging.error(f"[Connector] Could not send a message to node {node_id}!")
                port.is_enabled = False

    def node_registered(self, node_id: int) -> None:
        try:
            registered_port = self.ports_waiting.pop(0)
            registered_port.node_id = node_id
        except IndexError:
            logging.error("[Connector] Port is already registered!")

    async def _read_binary_message(self, port: SerialPort) -> None:
        while True:
            serial_port = next(filter(lambda x: x.name == port.name, self.serial_ports))
            is_binary, line = await serial_port.read_bytes()

            if line is None:
                port.is_enabled = False
                port.node_id = None
                return

            if len(line) == 0:
                await asyncio.sleep(3)
                continue

            if is_binary:
                self.handle_binary(port, line)
            else:
                self.handle_text(port, line)

    def handle_text(self, port: SerialPort, line: bytearray) -> None:
        line_text: str = line[:-1].decode('ISO-8859-1')

        if "main():" in line_text or "(Version:" in line_text:
            return

        logging.info(f"Text message from {port.name} -> {line_text}")

    def handle_binary(self, port: SerialPort, line: bytearray) -> None:
        logging.debug(f"Binary message from {port.name} -> {line[:-1]}")
        is_waiting_for_id = bool(next(filter(lambda x: x.name == port.name, self.ports_waiting), None))
        if port.node_id is None and not is_waiting_for_id:
            self.ports_waiting.append(port)

        self.message_queue.put_nowait(line)
