#!/usr/bin/env python3

import asyncio
import logging
from asyncio import Queue

import ttkbootstrap as ttk

from Orchestrator.AsyncTaskManager import AsyncTaskManager
from Orchestrator.Dashboard.AsyncTk import AsyncTk
from Orchestrator.Dashboard.Containers.NodeContainer import NodeContainer
from Orchestrator.Dashboard.Containers.ScriptContainer import ScriptContainer
from Orchestrator.Server.Connector.SerialConnector import SerialConnector
from Orchestrator.Server.EventBus.EventBus import EventBus
from Orchestrator.Server.MessageService.MessageService import MessageService
from Orchestrator.Server.NodeRegistry.NodeRegistry import NodeRegistry
from Orchestrator.Server.NodesScheduler.NodesScheduler import NodesScheduler
from Orchestrator.ServerRelay import ServerRelay


class App(AsyncTk):
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


async def main() -> None:
    async with asyncio.TaskGroup() as tg:
        # Asynchronous Task Manager
        async_task_manager = AsyncTaskManager(tg)

        # Connector
        message_queue = Queue()
        connector = SerialConnector(async_task_manager=async_task_manager,
                                    message_queue=message_queue)

        # Message Service
        message_service = MessageService(async_task_manager=async_task_manager,
                                         connector=connector,
                                         message_queue=message_queue)

        # Node Registry
        node_registry = NodeRegistry(async_task_manager=async_task_manager)

        # Node Scheduler
        nodes_scheduler = NodesScheduler()

        # Server Relay
        server_relay = ServerRelay()

        # Event Bus
        event_bus = EventBus(message_service=message_service,
                             node_registry=node_registry,
                             nodes_scheduler=nodes_scheduler,
                             server_relay=server_relay)
        message_service.set_event_bus(event_bus)
        nodes_scheduler.set_event_bus(event_bus)
        server_relay.set_event_bus(event_bus)

        # Application
        app = App(async_task_manager=async_task_manager, server_relay=server_relay)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-4s:  %(message)s',
        level=logging.NOTSET,
        datefmt='%Y-%m-%d %H:%M:%S')
    asyncio.run(main())
