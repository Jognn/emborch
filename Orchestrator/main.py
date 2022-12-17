import logging

import serial
from typing import Dict

from Orchestrator.Message import SendScriptMessage, MessageType, ORCHESTRATOR_ID
from Orchestrator.MessageService import MessageService
from Orchestrator.ScriptService import ScriptService

registered_devices: Dict[int, str] = {
    1: "ttyACM0"
}

# port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)

message_service = MessageService()
script_service = ScriptService("main.lua")

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-4s:  %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    lua_script = script_service.get_binary_script()
    send_script_msg = SendScriptMessage(type=MessageType.SendScript, sender=ORCHESTRATOR_ID, payload=lua_script)
    message_service.send_message(send_script_msg)
