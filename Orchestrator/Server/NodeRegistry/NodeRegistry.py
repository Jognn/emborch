import asyncio
import logging
from random import randint
from typing import Optional, List

from Orchestrator.AsyncTaskManager import AsyncTaskManager
from Orchestrator.Server.EventBus.Event import Event, EventType
from Orchestrator.Server.EventBus.EventComponent import EventComponent
from Orchestrator.Server.NodeRegistry.Node import Node


class NodeRegistry(EventComponent):
    STATUS_REQUEST_TIMEOUT_S = 10

    def __init__(self, async_task_manager: AsyncTaskManager):
        super().__init__()

        self.async_task_manager = async_task_manager
        self.available_ids = [i for i in range(14, 0, -1)]
        self.nodes = []

        self.adjectives = []
        self.names = []
        with open('Resources/adjectives.txt', 'r') as file:
            text: str = file.read()
            self.adjectives = text.lower().split("\n")

        with open('Resources/names.txt', 'r') as file:
            text: str = file.read()
            self.names = text.lower().split("\n")

    def register_new_node(self, available_memory_kb: int, supported_features: int) -> Optional[Node]:
        if len(self.available_ids) == 0:
            logging.error(f"[NodeRegistry] There are no more available ids left!")
            return None

        new_node_id = self.available_ids.pop()
        node = Node(node_id=new_node_id,
                    name=self._generate_random_name(),
                    available_memory_bytes=available_memory_kb * 1000,
                    supported_features=supported_features)
        self.nodes.append(node)
        self.async_task_manager.add_task(self._monitor_node(node))
        logging.info(f"[NodeRegistry] New node has been registered: {node}")
        return node

    def set_working_node(self, node_id: int, used_memory: int, script_text: str) -> None:
        node: Node = next(filter(lambda x: x.node_id == node_id, self.nodes), None)
        if node is None:
            return

        node.available_memory_bytes -= used_memory
        node.running_script = script_text

    def monitor_node_response(self, node_id: int):
        node: Node = next(filter(lambda x: x.node_id == node_id, self.nodes), None)
        if node is None:
            return

        node.status_queue.put(1)

    def get_nodes(self) -> List[Node]:
        return self.nodes

    async def _monitor_node(self, node: Node):
        while node.is_alive:
            try:
                monitor_node_request = Event(EventType.MONITOR_NODE)
                monitor_node_request.node_id = node.node_id
                self.event_bus.notify(monitor_node_request)

                status = await asyncio.wait_for(node.status_queue.get(), NodeRegistry.STATUS_REQUEST_TIMEOUT_S)
                logging.info(f"[NodeRegistry] Node {node.node_id} responded with MonitorNode status {status}")
            except TimeoutError:
                logging.error(f"[NodeRegistry] Node {node.node_id} did not respond to the MonitorNode request.")
                # self._unregister_node(node)

    def _unregister_node(self, node):
        node.is_alive = False
        self.nodes.remove(node)

    def _generate_random_name(self) -> str:
        adjectives_max_index = len(self.adjectives) - 1
        adjective = self.adjectives.pop(randint(0, adjectives_max_index))

        names_max_index = len(self.names) - 1
        name = self.names.pop(randint(0, names_max_index))

        return f"{adjective}_{name}"
