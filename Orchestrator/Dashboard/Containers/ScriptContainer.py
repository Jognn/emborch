from tkinter import Label, Button, Frame, Text

DEFAULT_SCRIPT_TEXT = "print('Hello world, this is lua!')"


class ScriptContainer:
    def __init__(self, root):
        self.root = root

        frame = Frame(root)
        frame.pack(padx=10, pady=10)

        label = Label(frame, text="In order to send your script press the below button")
        label.pack()

        self.text = Text(frame)
        self.text.insert('1.0', DEFAULT_SCRIPT_TEXT)
        self.text.pack()

        button = Button(root, text="Send script", command=self.send_script)
        button.pack()

    def send_script(self):
        SCRIPT_REQUIRED_MEMORY_MOCK = 12000
        self.root.server_relay.process_binary_script(self.text.get("1.0", 'end-1c'), 12000)
