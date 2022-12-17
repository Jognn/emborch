from typing import Type, TypeVar

from Orchestrator.Message import Message, SendScriptMessage, MessageType

END_OF_LINE_CHARACTER = b'\x17'


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

    def send_message(self, message: Type[M]) -> None:
        binary_message = self._generate_binary_message(message)
        with open("/dev/ttyACM0", "wb") as file:
            file.write(binary_message)

    def interpret_message(self, bytes):
        pass


if __name__ == "__main__":
    send_script_msg = SendScriptMessage(type=MessageType.SendScript,
                                        sender=15,
                                        payload=b'\x70\x72\x69\x6e\x74\x28\x22\x49\x20\x41\x4d\x20\x49\x4e\x20\x4c\x55')
    message_service = MessageService()
    msg = message_service.generate_message(send_script_msg)
    print(msg)
