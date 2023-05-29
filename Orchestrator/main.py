#!/usr/bin/env python3

import asyncio
import logging
from asyncio import Queue
from typing import Any, Coroutine

from Orchestrator.Dashboard.AsyncTk import AsyncTk
from Orchestrator.Dashboard.Containers.NodeContainer import NodeContainer
from Orchestrator.Dashboard.Containers.ScriptContainer import ScriptContainer
from Orchestrator.Server.Connector.Connector import Connector
from Orchestrator.Server.Connector.SerialConnector import SerialConnector
from Orchestrator.Server.EventBus.EventBus import EventBus
from Orchestrator.Server.MessageService.MessageService import MessageService
from Orchestrator.Server.NodeRegistry.NodeRegistry import NodeRegistry
from Orchestrator.Server.NodesScheduler.NodesScheduler import NodesScheduler
from Orchestrator.ServerRelay import ServerRelay


class App(AsyncTk):
    def __init__(self,
                 connector: Connector,
                 server_relay: ServerRelay,
                 poll_messages_coroutine: Coroutine[Any, Any, None]):
        super().__init__()

        # Server stuff
        connector.initialize(self.runners)
        self.runners.append(poll_messages_coroutine)

        # Dashboard stuff
        self.create_ui()
        self.server_relay = server_relay

        logging.info("emborch has started :)")

    def create_ui(self):
        self.title("Emborch dashboard")
        node_container = NodeContainer(self)
        script_container = ScriptContainer(self)


async def main(application: App):
    await application.run()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-4s:  %(message)s',
        level=logging.NOTSET,
        datefmt='%Y-%m-%d %H:%M:%S')
    # Connector
    message_queue = Queue()
    connector = SerialConnector(message_queue=message_queue)

    # Message Service
    message_service = MessageService(connector=connector, message_queue=message_queue)

    # Node Registry
    node_registry = NodeRegistry()

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
    app = App(connector=connector,
              server_relay=server_relay,
              poll_messages_coroutine=message_service.poll_messages())
    asyncio.run(main(app))
