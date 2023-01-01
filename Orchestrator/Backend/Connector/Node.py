import asyncio

from serial import Serial

DEVICE_DIRECTORY = "/dev/"


class Node:
    def __init__(self, name: str):
        self.name: str = name
        self.port = Serial(DEVICE_DIRECTORY + self.name, baudrate=115200, timeout=2.0)
        self.port.flush()
        self.connected: bool = False
        self.node_id: int = 0
        self.send_queue = asyncio.Queue()
