#!/usr/bin/env python3

import asyncio
import logging
from asyncio import Queue

from Orchestrator.Backend.Connector.Connector import Connector
from Orchestrator.Backend.Connector.SerialConnector import SerialConnector
from Orchestrator.Backend.MessageService.MessageService import MessageService
from Orchestrator.Backend.NodeRegistry.NodeRegistry import NodeRegistry
from Orchestrator.Backend.ScriptDispatcher.ScriptDispatcher import ScriptDispatcher
from Orchestrator.Frontend.AsyncTk import AsyncTk
from Orchestrator.Frontend.Widgets.ScriptContainer import ScriptContainer


class App(AsyncTk):
    def __init__(self, connector: Connector, script_dispatcher: ScriptDispatcher, message_service: MessageService):
        super().__init__()
        self.create_ui()
        self.script_dispatcher = script_dispatcher
        connector.initialize(self.runners)
        self.runners.append(message_service.poll_messages())

        logging.info("Orchestrator has started :)")

    def create_ui(self):
        a = ScriptContainer(self)
        a.show_items()


async def main(application: App):
    await application.run()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-4s:  %(message)s',
        level=logging.NOTSET,
        datefmt='%Y-%m-%d %H:%M:%S')

    message_queue = Queue()
    connector = SerialConnector(message_queue=message_queue)

    node_registry = NodeRegistry()
    message_service = MessageService(connector=connector, message_queue=message_queue, node_registry=node_registry)
    script_dispatcher = ScriptDispatcher(message_service=message_service, node_registry=node_registry)

    app = App(connector=connector, script_dispatcher=script_dispatcher, message_service=message_service)
    asyncio.run(main(app))
