from typing import List

from serial.tools.list_ports_linux import comports

from Orchestrator.Backend.Connector.PhysicalConnector import PhysicalConnector
from Orchestrator.Backend.Connector.SerialPort import SerialPort


class SerialConnector(PhysicalConnector):

    def __init__(self):
        comport_names = [comport.name for comport in comports() if "ACM" in comport.name]
        self.serial_ports = [SerialPort(name) for name in comport_names]

    async def read_message(self, port_name: str) -> (bool, bytearray):
        serial_port = next(filter(lambda port: port.name == port_name, self.serial_ports))
        return await serial_port.read_bytes()

    def send_message(self, port_name: str, binary_message: bytearray) -> None:
        # TODO: What if it does find a port with the provided port name? :)
        serial_port = next(filter(lambda port: port.name == port_name, self.serial_ports))
        serial_port.write(binary_message)

    def get_port_names(self) -> List[str]:
        # TODO: Shouldn't this only return names of comports with associated SerialPort objects?
        return [comport.name for comport in comports() if "ACM" in comport.name]
