import logging
from typing import Optional, List

from Orchestrator.Server.EventBus.EventComponent import EventComponent
from Orchestrator.Server.NodeRegistry.Node import Node


class NodesScheduler(EventComponent):
    def __init__(self):
        super().__init__()

    def choose_node(self, nodes: List[Node], script_required_memory: int) -> Optional[Node]:
        node = next(
            filter(lambda x: x.available_memory_bytes >= script_required_memory and x.running_script is None, nodes),
            None
        )
        if node is None:
            logging.info(
                f"[NodesScheduler] Could not find a suitable node for a {script_required_memory}B script."
                f"\n Node list: {nodes}")
        else:
            logging.info(f"[NodesScheduler] Node {node.node_id} has been assigned a new script!")
            return node
