import logging
from tkinter import ttk

from Orchestrator.AsyncTaskManager import AsyncTaskManager
from Orchestrator.Dashboard.AsyncTk import AsyncTk
from Orchestrator.Dashboard.Containers.NodeContainer import NodeContainer
from Orchestrator.Dashboard.Containers.ScriptContainer import ScriptContainer
from Orchestrator.ServerRelay import ServerRelay


class Dashboard(AsyncTk):
    def __init__(self, async_task_manager: AsyncTaskManager, server_relay: ServerRelay):
        super().__init__(async_task_manager=async_task_manager)

        # Server stuff
        self.server_relay = server_relay
        self.server_relay.set_dashboard(self)

        # Dashboard stuff
        self.title("Emborch dashboard")
        self.node_container = NodeContainer(self)

        separator = ttk.Separator(self, orient='horizontal', style='info.Horizontal.TSeparator')
        separator.pack(fill='x', pady=20)

        self.script_container = ScriptContainer(self)

        # MOCK!!!!!
        # self.add_new_node(node_id=20,
        #                   name="test_billy",
        #                   available_memory=1000,
        #                   supported_features=0)
        # MOCK

        logging.info("emborch has started :)")

    def add_new_node(self, node_id: int, name: str, available_memory: int, supported_features: int) -> None:
        self.node_container.add_node_entry(node_id, name, available_memory, supported_features)

    def node_assigned_script(self, node_id, available_memory: int, script_text: str):
        self.node_container.edit_node_entry(node_id=node_id,
                                            status="Occupied",
                                            available_memory=available_memory,
                                            script_txt=script_text)
