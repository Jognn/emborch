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

    def notify(self, event: Event) -> None:
        event_type = event.event_type

        if event_type == EventType.NODE_REGISTER:
            node: Optional[Node] = self.node_registry.register_new_node(event.available_memory,
                                                                        event.supported_features)
            if node is not None:
                self.message_service.send_register_result(node.node_id)
                self.server_relay.new_node_registered(node)
        elif event_type == EventType.SEND_SCRIPT:
            nodes = self.node_registry.get_nodes()
            chosen_node = self.nodes_scheduler.choose_node(nodes, event.required_memory)
            if chosen_node is not None:
                self.node_registry.set_working_node(chosen_node.node_id, event.required_memory, event.script_text)
                self.message_service.send_script_to_node(chosen_node, event.script_binary)
                self.server_relay.node_update(chosen_node)
        elif event_type == EventType.MONITOR_NODE:
            self.message_service.send_monitor_node_request(node_id=event.node_id)
        elif event_type == EventType.MONITOR_NODE_RESULT:
            self.node_registry.monitor_node_response(node_id=event.node_id, response=event.response)
        elif event_type == EventType.ALTER_NODE_STATE:
            self.server_relay.node_update(event.node)
        else:
            logging.error(f"[EventBus] Unknown event type: {event_type}")
