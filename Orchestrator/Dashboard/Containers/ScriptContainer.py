from tkinter import *
from tkinter.constants import *

DEFAULT_SCRIPT_TEXT = "print('Hello world, this is lua!')"


class ScriptContainer:
    def __init__(self, root):
        self.root = root

        frame = Frame(root)
        frame.pack(padx=10, pady=10)

        self.script_title = Label(frame, text="Task to run:")
        self.script_title.config(font=("Helvetica", "20", "bold"))
        self.script_title.pack()

        # Script text
        self.text = Text(frame)
        self.text.insert('1.0', DEFAULT_SCRIPT_TEXT)
        self.text.pack()

        # Required memory frame
        required_memory_frame = Frame(root, width=500)
        required_memory_frame.pack()

        required_memory_label = Label(required_memory_frame, text="Required memory (bytes): ")
        required_memory_label.pack(side=LEFT)

        self.required_memory_entry = Entry(required_memory_frame, justify=CENTER, width=8)
        self.required_memory_entry.insert(0, "12000")
        self.required_memory_entry.pack(side=RIGHT, padx=5)

        # Send script button
        button = Button(root, text="Send script", command=self.send_script)
        button.pack(pady=3)

    def send_script(self):
        self.root.server_relay.process_binary_script(
            self.text.get("1.0", 'end-1c'),
            int(self.required_memory_entry.get())
        )
