import asyncio

from serial import Serial, Timeout

EOT_SIGN = b'\x17'
EOL_SIGN = b'\x0A'

DEVICE_DIRECTORY = "/dev/"


class SerialPort(Serial):
    def __init__(self, name: str):
        super().__init__(DEVICE_DIRECTORY + name, baudrate=115200, timeout=2.0)
        self.name: str = name
        self.send_queue = asyncio.Queue()
        self.flush()

    async def read_bytes(self) -> (bool, bytearray):
        end_sign = (EOL_SIGN, EOT_SIGN)
        line = bytearray()
        timeout = Timeout(self._timeout)
        c = None
        while True:
            c = self.read(1)
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
