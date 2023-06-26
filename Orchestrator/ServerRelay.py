import logging

from Orchestrator.Server.EventBus.Event import Event, EventType
from Orchestrator.Server.EventBus.EventComponent import EventComponent
from Orchestrator.Server.NodeRegistry.Node import Node


class ServerRelay(EventComponent):
    def __init__(self):
        super().__init__()
        self.dashboard = None

    def set_dashboard(self, dashboard):
        self.dashboard = dashboard

    def process_binary_script(self, script_text: str, required_memory: int) -> None:
        logging.info(f'[ServerRelay] Loaded script (length = {len(script_text)}): \n{script_text}')

        compressed_text = self._compress_text(script_text)
        logging.info(f'[ServerRelay] Compressed script (length = {len(compressed_text)}): \n{compressed_text}')

        binary_script = bytearray()
        binary_script.extend(map(ord, compressed_text))

        send_script_event = Event()
        send_script_event.event_type = EventType.SEND_SCRIPT
        send_script_event.script_text = script_text
        send_script_event.required_memory = required_memory
        send_script_event.script_binary = binary_script
        self.event_bus.notify(send_script_event)

    def new_node_registered(self, node: Node) -> None:
        self.dashboard.add_new_node(node_id=node.node_id,
                                    name=node.name,
                                    state=node.state.value,
                                    available_memory=node.available_memory_bytes,
                                    supported_features=node.supported_features)

    def node_update(self, node: Node):
        self.dashboard.edit_node(node_id=node.node_id,
                                 state=node.state.value,
                                 available_memory=node.available_memory_bytes,
                                 script_text=node.running_script)

    def _compress_text(self, text: str) -> str:
        one_line_text = text.replace('\n', ' ').replace('\r', '')
        trimmed_one_line_text = filter(lambda x: x != '', one_line_text.split(' '))
        return ' '.join(trimmed_one_line_text)
