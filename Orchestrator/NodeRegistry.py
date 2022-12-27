import asyncio

from serial import Serial


DEVICE_DIRECTORY = "/dev/"


class Node:
    def     __init__(self, name: str):
        self.name: str = name
        self.port = Serial(DEVICE_DIRECTORY + self.name, baudrate=115200, timeout=3.0)
        self.connected: bool = False
        self.node_id: int = 0
        self.send_queue = asyncio.Queue()


class NodeRegistry:
    available_ids = [i for i in range(14, 0, -1)]

    @classmethod
    def register_new_node(cls, node: Node):
        # TODO: What if we run out of ids!
        # TODO: Check if the node is already registered!
        new_node_id = NodeRegistry.available_ids.pop()
        node.node_id = new_node_id
