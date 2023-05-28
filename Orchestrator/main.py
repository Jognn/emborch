#!/usr/bin/env python3

import asyncio
import logging
from asyncio import Queue

from Orchestrator.Dashboard.AsyncTk import AsyncTk
from Orchestrator.Dashboard.Containers.NodeContainer import NodeContainer
from Orchestrator.Dashboard.Containers.ScriptContainer import ScriptContainer
from Orchestrator.Server.Connector.Connector import Connector
from Orchestrator.Server.Connector.SerialConnector import SerialConnector
from Orchestrator.Server.MessageService.MessageService import MessageService
from Orchestrator.Server.NodeRegistry.NodeRegistry import NodeRegistry
from Orchestrator.Server.ScriptDispatcher.ScriptDispatcher import ScriptDispatcher
from Orchestrator.Server.ScriptDispatcher.ScriptService import ScriptService
from Orchestrator.ServerRelay import ServerRelay


class App(AsyncTk):
    def __init__(self, connector: Connector, script_dispatcher: ScriptDispatcher, message_service: MessageService):
        super().__init__()

        # Server stuff
        connector.initialize(self.runners)
        self.runners.append(message_service.poll_messages())

        # Dashboard stuff
        self.create_ui()
        self.script_dispatcher = script_dispatcher

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

    message_queue = Queue()

    # Connector
    connector = SerialConnector(message_queue=message_queue)

    # Node Registry
    node_registry = NodeRegistry()

    # Message Service
    message_service = MessageService(connector=connector, message_queue=message_queue, node_registry=node_registry)

    # Server Relay
    server_relay = ServerRelay()

    # Script dispatcher
    script_service = ScriptService()
    script_dispatcher = ScriptDispatcher(message_service=message_service,
                                         node_registry=node_registry,
                                         script_service=script_service)

    # Application
    app = App(connector=connector, script_dispatcher=script_dispatcher, message_service=message_service)
    asyncio.run(main(app))
