import asyncio
import logging
from typing import Type, TypeVar, Dict

from Orchestrator.Message import Message, SendScriptMessage, MessageType, RegisterMessage
from Orchestrator.NodeRegistry import Node, NodeRegistry
from Orchestrator.SerialConnector import SerialConnector
from Orchestrator.main import script_service

END_OF_LINE_CHARACTER = b'\x17'
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
            pass
        elif message.type == MessageType.SendScript:
            for byte in message.payload:
                binary_body.append(byte)
        elif message.type == MessageType.AliveCheck:
            pass
        elif message.type == MessageType.Report:
            pass

        binary_message.extend(binary_body)
        binary_message.extend(END_OF_LINE_CHARACTER)
        return binary_message

    def _interpret_message_and_respond(self, received_bytes: bytearray, node: Node) -> None:
        header = received_bytes[0]
        message_type = MessageType((header & MESSAGE_TYPE_MASK) >> 4)
        sender_id = (header & SENDER_ID_MASK)
        msg_response = Message()

        if message_type == MessageType.Register:
            NodeRegistry.register_new_node(node)
            msg_response = RegisterMessage(type=MessageType.Register,
                                           sender=ORCHESTRATOR_ID,
                                           assigned_id=node.node_id)
        elif message_type == MessageType.SendScript:
            pass
        elif message_type == MessageType.AliveCheck:
            pass
        elif message_type == MessageType.Report:
            pass

        binary_msg_response = self._generate_binary_message(msg_response)
        node.send_queue.put(binary_msg_response)

    async def read_message(self, node: Node):
        while True:
            is_binary, line = await SerialConnector.read_bytes(node)
            logging.info(f"Received new {'binary' if is_binary else 'text'} message from node {node.name} - \n{line}")

            if is_binary:
                self._interpret_message_and_respond(line, node)

    async def send_message(self, node: Node):
        while True:
            message = await node.send_queue.get()
            binary_message = self._generate_binary_message(message)
            with open("/dev/ttyACM0", "wb") as file:
                file.write(binary_message)


if __name__ == "__main__":
    send_script_msg = SendScriptMessage(type=MessageType.SendScript,
                                        sender=15,
                                        payload=b'\x70\x72\x69\x6e\x74\x28\x22\x49\x20\x41\x4d\x20\x49\x4e\x20\x4c\x55')
