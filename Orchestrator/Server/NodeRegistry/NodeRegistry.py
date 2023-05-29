from typing import Optional, List

from Orchestrator.Server.NodeRegistry.Node import Node


class NodeRegistry:
    def __init__(self):
        self.available_ids = [i for i in range(14, 0, -1)]
        self.nodes = []

    def register_new_node(self, available_memory: int, supported_features: int) -> Optional[Node]:
        # TODO: Check if the node is already registered!
        if len(self.available_ids) == 0:
            return None

        node = Node(available_memory, supported_features)
        new_node_id = self.available_ids.pop()
        node.node_id = new_node_id
        self.nodes.append(node)

        return node

    def working_node(self, node_id: int, used_memory: int, script_text: str) -> None:
        node = next(filter(lambda x: x.node_id == node_id, self.nodes), None)
        if node is not None:
            node.available_memory -= used_memory
            node.running_script = script_text

    def get_nodes(self) -> List[Node]:
        return self.nodes
