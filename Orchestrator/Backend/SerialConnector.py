from serial import Timeout
from serial.tools.list_ports_linux import comports

from Orchestrator.Backend.NodeRegistry import Node

EOT_SIGN = b'\x17'
EOL_SIGN = b'\x0A'


class SerialConnector:
    @classmethod
    async def read_bytes(cls, node: Node) -> (bool, bytearray):
        end_sign = (EOL_SIGN, EOT_SIGN)
        line = bytearray()
        timeout = Timeout(node.port._timeout)
        c = None
        while True:
            c = node.port.read(1)
            if c:
                line += c
                if c in end_sign:
                    break
            else:
                break
            if timeout.expired():
                break

        is_binary = c == EOT_SIGN

        return is_binary, line

    def __init__(self):
        comport_names = [comport.name for comport in comports() if "ACM" in comport.name]
        self.nodes = [Node(name) for name in comport_names]


if __name__ == '__main__':
    deviceService = SerialConnector()
