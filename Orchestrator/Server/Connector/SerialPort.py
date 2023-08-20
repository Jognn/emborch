import asyncio
import logging
from typing import Optional

from serial import Serial, SerialException

EOT_SIGN = b'\x17'
EOL_SIGN = b'\x0A'

DEVICE_DIRECTORY = "/dev/"


class SerialPort(Serial):
    def __init__(self, name: str):
        super().__init__(DEVICE_DIRECTORY + name, baudrate=115200, timeout=0.1)
        self.name: str = name
        self.send_queue = asyncio.Queue()
        self.node_id: Optional[int] = None
        self.is_enabled = True
        self.flush()

    async def read_bytes(self) -> (bool, bytearray):
        end_sign = (EOL_SIGN, EOT_SIGN)
        line = bytearray()
        is_binary = False
        try:
            while True:
                c = self.read()
                if c:
                    line += c
                    if c in end_sign:
                        break
                else:
                    break
            is_binary = (c == EOT_SIGN)
        except:
            is_binary = False
            line = None
        finally:
            return is_binary, line

    def write(self, binary_message: bytearray) -> Optional[int]:
        try:
            binary_message.extend(EOT_SIGN)
            return super().write(binary_message)
        except SerialException as exception:
            logging.error(exception)
            return None
