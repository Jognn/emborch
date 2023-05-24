from Orchestrator.Server.MessageService import MessageService
from Orchestrator.Server.NodeRegistry import NodeRegistry
from Orchestrator.Server.NodeRegistry.Node import Node
from Orchestrator.Server.ScriptDispatcher.ScriptService import ScriptService


class ScriptDispatcher:
    def __init__(self, message_service: MessageService, node_registry: NodeRegistry, script_service: ScriptService):
        self.message_service = message_service
        self.node_registry = node_registry
        self.script_service = script_service

    def _choose_node(self) -> Node:
        return self.node_registry.nodes[0]

    def send_script(self, script_text: str) -> None:
        chosen_node = self._choose_node()
        binary_script = self.script_service.get_binary_script(script_text)
        self.message_service.send_script_to_node(chosen_node, binary_script)
