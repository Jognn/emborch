#!/usr/bin/env python3.11

import asyncio
import logging
import sys
from asyncio import Queue

from Orchestrator.AsyncTaskManager import AsyncTaskManager
from Orchestrator.Dashboard.Dashboard import Dashboard
from Orchestrator.Server.Connector.SerialConnector import SerialConnector
from Orchestrator.Server.EventBus.EventBus import EventBus
from Orchestrator.Server.MessageService.MessageService import MessageService
from Orchestrator.Server.NodeRegistry.NodeRegistry import NodeRegistry
from Orchestrator.Server.NodesScheduler.NodesScheduler import NodesScheduler
from Orchestrator.ServerRelay import ServerRelay


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
        node_registry.set_event_bus(event_bus)
        nodes_scheduler.set_event_bus(event_bus)
        server_relay.set_event_bus(event_bus)

        # Dashboard GUI
        dashboard = Dashboard(async_task_manager=async_task_manager, server_relay=server_relay)


if __name__ == '__main__':
    python_number = sys.version_info[0]
    python_version = sys.version_info[1]
    if python_number < 3 or python_version < 11:
        raise Exception("Requires Python 3.11 or higher!")

    logging.basicConfig(
        format='%(asctime)s %(levelname)-4s:  %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    asyncio.run(main())
