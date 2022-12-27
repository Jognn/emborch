from Orchestrator.Backend.Node import Node


class NodeRegistry:
    available_ids = [i for i in range(14, 0, -1)]

    @classmethod
    def register_new_node(cls, node: Node):
        # TODO: What if we run out of ids!
        # TODO: Check if the node is already registered!
        new_node_id = NodeRegistry.available_ids.pop()
        node.node_id = new_node_id
