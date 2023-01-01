#!/usr/bin/env python3

import asyncio
import logging

from Orchestrator.Backend.Connector.SerialConnector import serial_connector
from Orchestrator.Backend.MessageService.MessageService import message_service
from Orchestrator.Frontend.AsyncTk import AsyncTk
from Orchestrator.Frontend.Widgets.ScriptContainer import ScriptContainer


class App(AsyncTk):

    def __init__(self):
        super().__init__()
        self.create_interface()
        nodes = serial_connector.nodes
        for node in nodes:
            self.runners.append(message_service.read_message(node))
            self.runners.append(message_service.send_message(node))
        logging.info("Orchestrator has started :)")

    def create_interface(self):
        a = ScriptContainer(self)
        a.show_items()


async def main():
    app = App()
    await app.run()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-4s:  %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    asyncio.run(main())
