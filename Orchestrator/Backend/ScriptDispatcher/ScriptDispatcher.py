from Orchestrator.Backend.MessageService import MessageService
from Orchestrator.Backend.NodeRegistry import NodeRegistry
from Orchestrator.Backend.NodeRegistry.Node import Node
from Orchestrator.Backend.ScriptDispatcher.ScriptService import script_service


class ScriptDispatcher:
    def __init__(self, message_service: MessageService, node_registry: NodeRegistry):
        self.message_service = message_service
        self.node_registry = node_registry

    def _choose_node(self) -> Node:
        return self.node_registry.nodes[0]

    def send_script(self) -> None:
        chosen_node = self._choose_node()
        binary_script = script_service.get_binary_script()
        self.message_service.send_script_to_node(chosen_node, binary_script)
