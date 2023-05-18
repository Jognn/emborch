import asyncio
import logging
from asyncio import Queue
from typing import TypeVar, Optional

from Orchestrator.Backend.Connector.Connector import Connector
from Orchestrator.Backend.MessageService.Message import Message, SendScriptMessage, MessageType, RegisterMessage
from Orchestrator.Backend.NodeRegistry import NodeRegistry
from Orchestrator.Backend.NodeRegistry.Node import Node

MESSAGE_TYPE_MASK = 240
SENDER_ID_MASK = 15
ORCHESTRATOR_ID = 15


class MessageService:
    MessageType = TypeVar('MessageType', bound=Message)

    def __init__(self, connector: Connector, message_queue: Queue, node_registry: NodeRegistry):
        self.connector = connector
        self.message_queue = message_queue
        self.node_registry = node_registry

    async def poll_messages(self) -> None:
        while True:
            if self.message_queue.empty():
                await asyncio.sleep(1)
                continue

            binary_message = await self.message_queue.get()
            message = self._interpret_message_and_generate_response(binary_message)
            if message is None:
                continue

            if message.type == MessageType.Register:
                binary_message_response = self._generate_binary_message(message)
                self.connector.send_binary_message(message.assigned_id, binary_message_response)

    def send_script_to_node(self, node: Node, binary_script: bytearray):
        send_script_msg = SendScriptMessage(type=MessageType.SendScript, sender=ORCHESTRATOR_ID, payload=binary_script)
        binary_msg = self._generate_binary_message(send_script_msg)
        self.connector.send_binary_message(node.node_id, binary_msg)

    def _generate_binary_message(self, message: Message) -> bytearray:
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
            logging.error("Generating AliveCheck message is not supported yet!")
        elif message.type == MessageType.Report:
            logging.error("Generating Report message is not supported yet!")
        else:
            logging.error("Generating unsupported message type!")
        binary_message.extend(binary_body)

        return binary_message

    def _interpret_message_and_generate_response(self, received_bytes: bytearray) -> Optional[RegisterMessage]:
        header = received_bytes[0]
        message_type = MessageType((header & MESSAGE_TYPE_MASK) >> 4)
        sender_id = (header & SENDER_ID_MASK)

        if message_type == MessageType.Register:
            logging.info("New Register message has arrived!")
            new_node = self.node_registry.register_new_node(int(received_bytes[1]))
            return RegisterMessage(type=MessageType.Register,
                                   sender=ORCHESTRATOR_ID,
                                   assigned_id=new_node.node_id)
        elif message_type == MessageType.SendScript:
            logging.error("Interpreting SendScript message is not supported yet!")
            return None
        elif message_type == MessageType.AliveCheck:
            logging.error("Interpreting AliveCheck message is not supported yet!")
            return None
        elif message_type == MessageType.Report:
            logging.error("Interpreting Report message is not supported yet!")
            return None
        else:
            logging.error("Interpreting unsupported message type!")
            return None


if __name__ == "__main__":
    msg = SendScriptMessage(type=MessageType.SendScript,
                            sender=15,
                            payload=b'\x70\x72\x69\x6e\x74\x28\x22\x49\x20\x41\x4d\x20\x49\x4e\x20\x4c\x55')
