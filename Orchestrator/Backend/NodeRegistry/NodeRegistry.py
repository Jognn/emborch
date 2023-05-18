from Orchestrator.Backend.NodeRegistry.Node import Node


class NodeRegistry:
    def __init__(self):
        self.available_ids = [i for i in range(14, 0, -1)]
        self.nodes = []

    def register_new_node(self, available_memory: int) -> Node:
        # TODO: What if we run out of ids!
        # TODO: Check if the node is already registered!
        node = Node(available_memory)
        new_node_id = self.available_ids.pop()
        node.node_id = new_node_id
        self.nodes.append(node)

        return node
