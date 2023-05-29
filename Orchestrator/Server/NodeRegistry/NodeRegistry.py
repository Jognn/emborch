import logging
from typing import Optional, List

from Orchestrator.Server.NodeRegistry.Node import Node


class NodeRegistry:
    def __init__(self):
        self.available_ids = [i for i in range(14, 0, -1)]
        self.nodes = []

    def register_new_node(self, available_memory_kb: int, supported_features: int) -> Optional[Node]:
        # TODO: Check if the node is already registered!
        if len(self.available_ids) == 0:
            return None

        new_node_id = self.available_ids.pop()
        node = Node(node_id=new_node_id,
                    available_memory_bytes=available_memory_kb * 1000,
                    supported_features=supported_features)
        self.nodes.append(node)
        logging.info(f"[NodeRegistry] New node has been registered: {node}")
        return node

    def working_node(self, node_id: int, used_memory: int, script_text: str) -> None:
        node = next(filter(lambda x: x.node_id == node_id, self.nodes), None)
        if node is not None:
            node.available_memory_bytes -= used_memory
            node.running_script = script_text

    def get_nodes(self) -> List[Node]:
        return self.nodes
