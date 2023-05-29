import asyncio
from typing import Optional

from serial import Serial

EOT_SIGN = b'\x17'
EOL_SIGN = b'\x0A'

DEVICE_DIRECTORY = "/dev/"


class SerialPort(Serial):
    def __init__(self, name: str):
        super().__init__(DEVICE_DIRECTORY + name, baudrate=115200, timeout=0.1)
        self.name: str = name
        self.send_queue = asyncio.Queue()
        self.node_id: Optional[int] = None
        self.flush()

    async def read_bytes(self) -> (bool, bytearray):
        end_sign = (EOL_SIGN, EOT_SIGN)
        line = bytearray()
        while True:
            c = self.read()
            if c:
                line += c
                if c in end_sign:
                    break
            else:
                break

        is_binary = (c == EOT_SIGN)
        return is_binary, line

    def write(self, binary_message: bytearray) -> int:
        binary_message.extend(EOT_SIGN)
        return super().write(binary_message)
