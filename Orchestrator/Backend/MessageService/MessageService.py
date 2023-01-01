import asyncio
import logging
from typing import Type, TypeVar

from Orchestrator.Backend.Connector.Node import Node
from Orchestrator.Backend.Connector.SerialConnector import SerialConnector, EOT_SIGN
from Orchestrator.Backend.MessageService.Message import Message, SendScriptMessage, MessageType, RegisterMessage
from Orchestrator.Backend.NodeRegistry.NodeRegistry import NodeRegistry

MESSAGE_TYPE_MASK = 240
SENDER_ID_MASK = 15
ORCHESTRATOR_ID = 15


class MessageService:
    M = TypeVar('M', bound=Message)

    def _generate_binary_message(self, message: Type[M]) -> bytearray:
        binary_message = bytearray()

        # Header
        binary_header = (message.type.value & 15) << 4 | message.sender & 15
        binary_message.append(binary_header)

        # Body
        binary_body = bytearray()
        if message.type == MessageType.Register:
            binary_body.append(message.assigned_id)
        elif message.type == MessageType.SendScript:
            for byte in message.payload:
                binary_body.append(byte)
        elif message.type == MessageType.AliveCheck:
            logging.error("Generating Report message is not supported yet!")
        elif message.type == MessageType.Report:
            pass
        else:
            logging.error("Generating unsupported message type!")

        binary_message.extend(binary_body)
        binary_message.extend(EOT_SIGN)
        return binary_message

    def _interpret_message_and_respond(self, received_bytes: bytearray, node: Node) -> RegisterMessage | None:
        header = received_bytes[0]
        message_type = MessageType((header & MESSAGE_TYPE_MASK) >> 4)
        sender_id = (header & SENDER_ID_MASK)

        if message_type == MessageType.Register:
            logging.info("New Register message has arrived!")
            NodeRegistry.register_new_node(node)
            return RegisterMessage(type=MessageType.Register,
                                   sender=ORCHESTRATOR_ID,
                                   assigned_id=node.node_id)
        elif message_type == MessageType.SendScript:
            logging.error("Interpreting SendScript message is not supported yet!")
            return
        elif message_type == MessageType.AliveCheck:
            logging.error("Interpreting AliveCheck message is not supported yet!")
            return
        elif message_type == MessageType.Report:
            logging.error("Interpreting Report message is not supported yet!")
            return
        else:
            logging.error("Interpreting unsupported message type!")
            return

    async def read_message(self, node: Node):
        while True:
            is_binary, line = await SerialConnector.read_bytes(node)

            if line:
                logging.info(
                    f"{'Binary' if is_binary else 'Text'} message from {node.name}"
                    f" -> {line if is_binary else line[:-1].decode('ISO-8859-1')}")

                if is_binary:
                    if msg_response := self._interpret_message_and_respond(line, node):
                        await node.send_queue.put(msg_response)
                await asyncio.sleep(0.5)
            else:
                await asyncio.sleep(3)

    async def send_message(self, node: Node):
        while True:
            if node.send_queue.empty():
                await asyncio.sleep(5)
                continue
            message = await node.send_queue.get()
            binary_message = self._generate_binary_message(message)
            logging.info(f"Sending new binary message to {node.name} -> {binary_message}")
            node.port.write(binary_message)


message_service = MessageService()

if __name__ == "__main__":
    send_script_msg = SendScriptMessage(type=MessageType.SendScript,
                                        sender=15,
                                        payload=b'\x70\x72\x69\x6e\x74\x28\x22\x49\x20\x41\x4d\x20\x49\x4e\x20\x4c\x55')
