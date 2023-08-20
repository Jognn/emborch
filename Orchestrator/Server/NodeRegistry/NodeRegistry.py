import asyncio
import logging
from random import randint
from typing import Optional, List

from Orchestrator.AsyncTaskManager import AsyncTaskManager
from Orchestrator.Server.EventBus.Event import Event, EventType
from Orchestrator.Server.EventBus.EventComponent import EventComponent
from Orchestrator.Server.NodeRegistry.Node import Node, NodeState


class NodeRegistry(EventComponent):
    REQUEST_MONITOR_NODE_INTERVAL_S = 10
    STATUS_REQUEST_TIMEOUT_S = REQUEST_MONITOR_NODE_INTERVAL_S * 2

    def __init__(self, async_task_manager: AsyncTaskManager):
        super().__init__()

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

    def register_new_node(self, available_memory_kb: int, supported_features: int) -> Optional[Node]:
        if len(self.available_ids) == 0:
            logging.error(f"[NodeRegistry] There are no more available ids left!")
            return None

        new_node_id = self.available_ids.pop()
        node = Node(node_id=new_node_id,
                    name=self._generate_random_name(),
                    initial_memory_bytes=available_memory_kb * 1000,
                    supported_features=supported_features,
                    status_queue=asyncio.Queue(maxsize=1))
        self.nodes.append(node)
        self.async_task_manager.add_task(self._monitor_node(node))
        logging.info(f"[NodeRegistry] New node has been registered: {node}")
        return node

    def set_working_node(self, node_id: int, used_memory: int, script_text: str) -> None:
        node: Node = next(filter(lambda x: x.node_id == node_id, self.nodes), None)
        if node is not None:
            node.available_memory_bytes -= used_memory
            node.running_script = script_text
            node.state = NodeState.Working

    def monitor_node_response(self, node_id: int, response: int):
        node: Node = next(filter(lambda x: x.node_id == node_id, self.nodes), None)
        if node is not None:
            node.status_queue.put_nowait(response)
        else:
            logging.error(f"Did not expect a monitor response for Node {node_id}")

    def get_nodes(self) -> List[Node]:
        return self.nodes

    async def _monitor_node(self, node: Node):
        first_iteration = True
        while node.state in (NodeState.Connected, NodeState.Working) or first_iteration:
            try:
                await asyncio.sleep(NodeRegistry.REQUEST_MONITOR_NODE_INTERVAL_S)

                logging.info(f"[NodeRegistry] Sending MonitorNode request to node {node.node_id}")
                monitor_node_request = Event(EventType.MONITOR_NODE)
                monitor_node_request.node_id = node.node_id
                self.event_bus.notify(monitor_node_request)

                status_code = await asyncio.wait_for(node.status_queue.get(), NodeRegistry.STATUS_REQUEST_TIMEOUT_S)
                logging.info(f"[NodeRegistry] Node {node.node_id} responded with status code {status_code}")
                self._update_node_after_status(node, status_code)
            except TimeoutError:
                logging.error(f"[NodeRegistry] Node {node.node_id} did not respond to the 'Monitor' request!")
                self._unregister_node(node)
                if node.running_script is not None:
                    send_script_event = Event()
                    send_script_event.event_type = EventType.SEND_SCRIPT
                    send_script_event.script_text = node.running_script
                    send_script_event.required_memory = node.initial_memory_bytes - node.available_memory_bytes
                    script_binary = bytearray()
                    script_binary.extend(map(ord, node.running_script))
                    send_script_event.script_binary = script_binary
                    self.event_bus.notify(send_script_event)
            finally:
                alter_node_state_event = Event(EventType.ALTER_NODE_STATE)
                alter_node_state_event.node = node
                self.event_bus.notify(alter_node_state_event)
                first_iteration = False

    def _update_node_after_status(self, node: Node, status_code: int) -> None:
        if status_code == 255:
            if node.running_script is not None:
                node.available_memory_bytes = node.initial_memory_bytes
            node.running_script = None
            node.state = NodeState.Connected
        elif status_code == 0:
            node.state = NodeState.Working
        else:
            node.state = NodeState.Error
            node.running_script = None
            node.available_memory_bytes = node.initial_memory_bytes

    def _unregister_node(self, node: Node) -> None:
        node.state = NodeState.Disconnected
        self.nodes.remove(node)

    def _generate_random_name(self) -> str:
        adjectives_max_index = len(self.adjectives) - 1
        adjective = self.adjectives.pop(randint(0, adjectives_max_index))

        names_max_index = len(self.names) - 1
        name = self.names.pop(randint(0, names_max_index))

        return f"{adjective}_{name}"
