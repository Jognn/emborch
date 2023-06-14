import asyncio
import logging
from asyncio import Queue
from typing import TypeVar, Optional

from Orchestrator.AsyncTaskManager import AsyncTaskManager
from Orchestrator.Server.Connector.Connector import Connector
from Orchestrator.Server.EventBus.Event import Event, EventType
from Orchestrator.Server.EventBus.EventComponent import EventComponent
from Orchestrator.Server.MessageService.Message import Message, SendScriptMessage, MessageType, RegisterMessage
from Orchestrator.Server.NodeRegistry.Node import Node

MESSAGE_TYPE_MASK = 240
SENDER_ID_MASK = 15
ORCHESTRATOR_ID = 15


class MessageService(EventComponent):
    MessageType = TypeVar('MessageType', bound=Message)

    def __init__(self, async_task_manager: AsyncTaskManager, connector: Connector, message_queue: Queue):
        super().__init__()

        self.async_task_manager = async_task_manager
        self.connector = connector
        self.message_queue = message_queue

        self.async_task_manager.add_task(self.poll_messages())

    async def poll_messages(self) -> None:
        while True:
            if self.message_queue.empty():
                await asyncio.sleep(1)
                continue

            binary_message = await self.message_queue.get()
            self._handle_message(binary_message)

    def send_script_to_node(self, node: Node, binary_script: bytearray) -> None:
        send_script_msg = SendScriptMessage(type=MessageType.SendScript, sender=ORCHESTRATOR_ID, payload=binary_script)
        binary_msg = self._generate_binary_message(send_script_msg)
        self.connector.send_binary_message(node.node_id, binary_msg)

    def send_register_result(self, node: Optional[Node]) -> None:
        if node is not None:
            self.connector.node_registered(node.node_id)

        register_message = RegisterMessage(type=MessageType.Register,
                                           sender=ORCHESTRATOR_ID,
                                           assigned_id=node.node_id if node is not None else ORCHESTRATOR_ID)
        binary_message_response = self._generate_binary_message(register_message)

        self.connector.send_binary_message(register_message.assigned_id, binary_message_response)

    def _generate_binary_message(self, message: Message) -> bytearray:
        binary_message = bytearray()

        # Header
        message_type = (message.type.value & 0xF) << 4
        message_sender = message.sender & 0xF
        binary_header = message_type | message_sender
        binary_message.append(binary_header)

        # Body
        binary_body = bytearray()
        if message.type == MessageType.Register:
            binary_body.append(message.assigned_id)
        elif message.type == MessageType.SendScript:
            for byte in message.payload:
                binary_body.append(byte)
        elif message.type == MessageType.AliveCheck:
            logging.error("[MessageService] Generating AliveCheck message is not supported yet!")
        elif message.type == MessageType.Report:
            logging.error("[MessageService] Generating Report message is not supported yet!")
        else:
            logging.error("[MessageService] Generating unsupported message type!")
        binary_message.extend(binary_body)

        return binary_message

    def _handle_message(self, received_bytes: bytearray) -> Optional[RegisterMessage]:
        header = received_bytes[0]
        message_type = MessageType((header & MESSAGE_TYPE_MASK) >> 4)
        sender_id = (header & SENDER_ID_MASK)

        event = Event()
        if message_type == MessageType.Register:
            logging.info("[MessageService] New Register message has arrived!")
            event.event_type = EventType.NODE_REGISTER
            event.available_memory = int(received_bytes[1])
            # TODO: Support 'Supported features' :)
            # event.supported_features = int(received_bytes[2] + received_bytes[3])
            event.supported_features = 0
            self.event_bus.notify(event)
        elif message_type == MessageType.SendScript:
            logging.error("[MessageService] Interpreting SendScript message is not supported yet!")
            return None
        elif message_type == MessageType.AliveCheck:
            logging.error("[MessageService] Interpreting AliveCheck message is not supported yet!")
            return None
        elif message_type == MessageType.Report:
            logging.error("[MessageService] Interpreting Report message is not supported yet!")
            return None
        else:
            logging.error("[MessageService] Interpreting unsupported message type!")
            return None


if __name__ == "__main__":
    msg = SendScriptMessage(type=MessageType.SendScript,
                            sender=15,
                            payload=b'\x70\x72\x69\x6e\x74\x28\x22\x49\x20\x41\x4d\x20\x49\x4e\x20\x4c\x55')
