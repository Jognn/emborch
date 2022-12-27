#!/usr/bin/env python3

import asyncio
import logging

from Orchestrator.Backend.MessageService import MessageService
from Orchestrator.Backend.ScriptService import ScriptService
from Orchestrator.Backend.SerialConnector import SerialConnector
from Orchestrator.Frontend.AsyncTk import AsyncTk

serial_connector = SerialConnector()
message_service = MessageService()
script_service = ScriptService("main.lua")


class App(AsyncTk):
    "User's app"

    def __init__(self):
        super().__init__()
        self.create_interface()
        nodes = serial_connector.nodes
        for node in nodes:
            self.runners.append(message_service.read_message(node))
            self.runners.append(message_service.send_message(node))
        logging.info("Orchestrator has started :)")

    def create_interface(self):
        pass


async def main():
    app = App()
    await app.run()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-4s:  %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    asyncio.run(main())

# lua_script = script_service.get_binary_script()
# send_script_msg = SendScriptMessage(type=MessageType.SendScript, sender=ORCHESTRATOR_ID, payload=lua_script)
# message_service.send_message(send_script_msg)
