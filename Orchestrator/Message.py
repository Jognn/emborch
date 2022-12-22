from enum import Enum

ORCHESTRATOR_ID = 15


class MessageType(Enum):
    Register = 0
    SendScript = 1
    AliveCheck = 2
    Report = 3


class Message:
    def __init__(self, **kwargs):
        self.type = kwargs['type']
        self.sender = kwargs['sender']


class RegisterMessage(Message):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.assigned_id = kwargs['assigned_id']


class SendScriptMessage(Message):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payload = kwargs['payload']
