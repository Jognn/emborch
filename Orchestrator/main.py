import logging

import asyncio

from Orchestrator.MessageService import MessageService
from Orchestrator.ScriptService import ScriptService
from Orchestrator.SerialConnector import SerialConnector

serial_connector = SerialConnector()
message_service = MessageService()
script_service = ScriptService("main.lua")


async def main():
    tasks = list()
    nodes = serial_connector.nodes
    for node in nodes:
        read_task = asyncio.create_task(message_service.read_message(node))
        tasks.append(read_task)

        send_task = asyncio.create_task(message_service.send_message(node))
        tasks.append(send_task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-4s:  %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info("Orchestrator has started :)")
    # lua_script = script_service.get_binary_script()
    # send_script_msg = SendScriptMessage(type=MessageType.SendScript, sender=ORCHESTRATOR_ID, payload=lua_script)
    # message_service.send_message(send_script_msg)
    asyncio.run(main())
