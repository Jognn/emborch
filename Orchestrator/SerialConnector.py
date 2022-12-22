import logging
from asyncio import Event
from typing import Type

from serial.tools.list_ports_linux import comports

from Orchestrator.NodeRegistry import Node

EOT_SIGN = b'\x1F'
EOL_SIGN = b'\x0A'


class SerialConnector:
    @classmethod
    async def read_bytes(cls, node: Node) -> (bool, bytearray):
        end_sign = (EOL_SIGN, EOT_SIGN)
        line = bytearray()
        c = None
        while True:
            c = node.port.read(1)
            if c:
                line += c
                if c in end_sign:
                    break

        is_binary = c == EOT_SIGN

        return is_binary, line

    def __init__(self):
        comport_names = [comport.name for comport in comports() if "ACM" in comport.name]
        self.nodes = [Node(name) for name in comport_names]


if __name__ == '__main__':
    deviceService = SerialConnector()
