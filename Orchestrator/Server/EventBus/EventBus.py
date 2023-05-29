import logging
from typing import Optional

from Orchestrator.Server.EventBus.Event import Event, EventType
from Orchestrator.Server.MessageService.MessageService import MessageService
from Orchestrator.Server.NodeRegistry.Node import Node
from Orchestrator.Server.NodeRegistry.NodeRegistry import NodeRegistry
from Orchestrator.Server.NodesScheduler.NodesScheduler import NodesScheduler
from Orchestrator.ServerRelay import ServerRelay


class EventBus:
    def __init__(self,
                 message_service: MessageService,
                 node_registry: NodeRegistry,
                 nodes_scheduler: NodesScheduler,
                 server_relay: ServerRelay):
        self.message_service = message_service
        self.node_registry = node_registry
        self.nodes_scheduler = nodes_scheduler
        self.server_relay = server_relay

    def notify(self, event: Event):
        event_type = event.event_type

        if event_type == EventType.NODE_REGISTER:
            node: Optional[Node] = self.node_registry.register_new_node(event.available_memory,
                                                                        event.supported_features)
            self.message_service.send_register_result(node)
        elif event_type == EventType.SEND_SCRIPT:
            nodes = self.node_registry.get_nodes()
            chosen_node = self.nodes_scheduler.choose_node(nodes, event.required_memory)
            if chosen_node is not None:
                self.node_registry.working_node(chosen_node.node_id, event.required_memory, event.script_text)
                self.message_service.send_script_to_node(chosen_node, event.script_binary)
        else:
            logging.error(f"[EventBus] Unknown event type: {event_type}")
