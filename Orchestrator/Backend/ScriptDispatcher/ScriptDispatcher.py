from Orchestrator.Backend.Connector.Node import Node
from Orchestrator.Backend.Connector.SerialConnector import serial_connector
from Orchestrator.Backend.MessageService.Message import SendScriptMessage, MessageType, ORCHESTRATOR_ID
from Orchestrator.Backend.ScriptDispatcher.ScriptService import script_service


class ScriptDispatcher:

    def _choose_node(self) -> Node:
        return serial_connector.nodes[0]

    def send_script(self) -> None:
        node = self._choose_node()
        lua_script = script_service.get_binary_script()
        send_script_msg = SendScriptMessage(type=MessageType.SendScript, sender=ORCHESTRATOR_ID, payload=lua_script)
        node.send_queue.put_nowait(send_script_msg)


script_dispatcher = ScriptDispatcher()
