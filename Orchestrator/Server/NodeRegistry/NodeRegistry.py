import asyncio
import logging
from copy import deepcopy
from random import randint
from typing import Optional, List

from Orchestrator.AsyncTaskManager import AsyncTaskManager
from Orchestrator.Server.NodeRegistry.Node import Node


class NodeRegistry:
    def __init__(self, async_task_manager: AsyncTaskManager):
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

        self.async_task_manager.add_task(self._monitor_nodes())

    def register_new_node(self, available_memory_kb: int, supported_features: int) -> Optional[Node]:
        # TODO: Check if the node is already registered!
        if len(self.available_ids) == 0:
            return None

        new_node_id = self.available_ids.pop()
        node = Node(node_id=new_node_id,
                    name=self._generate_random_name(),
                    available_memory_bytes=available_memory_kb * 1000,
                    supported_features=supported_features)
        self.nodes.append(node)
        logging.info(f"[NodeRegistry] New node has been registered: {node}")
        return node

    def set_working_node(self, node_id: int, used_memory: int, script_text: str) -> None:
        node = next(filter(lambda x: x.node_id == node_id, self.nodes), None)
        if node is not None:
            node.available_memory_bytes -= used_memory
            node.running_script = script_text

    def get_nodes(self) -> List[Node]:
        return self.nodes

    async def _monitor_nodes(self):
        while True:
            current_nodes = deepcopy(self.nodes)

            if len(current_nodes) == 0:
                print("NO NODES")
                await asyncio.sleep(10)

            for node in current_nodes:
                # TODO: If they are separate tasks for sending ALIVE_CHECK and interpreting it,
                # they could be a synchronisation issue, in which the interpreting tasks marks node invalid,
                # but the "sending" one does not know it yet!
                print(f"MONITORING NODE {node.node_id}")
                await asyncio.sleep(10)

    def _generate_random_name(self) -> str:
        adjectives_max_index = len(self.adjectives) - 1
        adjective = self.adjectives.pop(randint(0, adjectives_max_index))

        names_max_index = len(self.names) - 1
        name = self.names.pop(randint(0, names_max_index))

        return f"{adjective}_{name}"
