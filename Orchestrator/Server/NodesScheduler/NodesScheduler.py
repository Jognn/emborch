import logging
from typing import Optional, List

from Orchestrator.Server.EventBus.EventComponent import EventComponent
from Orchestrator.Server.NodeRegistry.Node import Node


class NodesScheduler(EventComponent):
    def __init__(self):
        super().__init__()

    def choose_node(self, nodes: List[Node], script_required_memory: int) -> Optional[Node]:
        if len(nodes) > 0:
            logging.info(f"[NodesScheduler] Node {nodes[0].node_id} is now running a new script!")
            return nodes[0]
        else:
            logging.info(
                f"[NodesScheduler] Could not find a suitable node ({nodes}) for a {script_required_memory}B script")
            return None
