from tkinter import Label, Button

from Orchestrator.Backend.ScriptDispatcher.ScriptDispatcher import script_dispatcher
from Orchestrator.Frontend.Widgets.Widget import Widget


class ScriptContainer(Widget):
    def __init__(self, master):
        super().__init__(master)

        master.title("Orchestrator GUI")

        self.items.append(Label(master, text="In order to send your script press the below button"))
        self.items.append(Button(master, text="Send script", command=self.send_script))

    def send_script(self):
        script_dispatcher.send_script()
