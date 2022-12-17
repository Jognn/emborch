import serial
from typing import Dict

from Orchestrator.Message import SendScriptMessage, MessageType, ORCHESTRATOR_ID
from Orchestrator.MessageService import MessageService

registered_devices: Dict[int, str] = {
    1: "ttyACM0"
}

port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)

message_service = MessageService()

if __name__ == "__main__":
    lua_script = b'\x70\x72\x69\x6e\x74\x28\x22\x49\x20\x41\x4d\x20\x49\x4e\x20\x4c\x55\x41\x21\x22\x29\x0a'
    send_script_msg = SendScriptMessage(type=MessageType.SendScript, sender=ORCHESTRATOR_ID, payload=lua_script)
    message_service.send_message(send_script_msg)