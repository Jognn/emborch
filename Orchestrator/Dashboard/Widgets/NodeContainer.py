from tkinter import Frame, Label
from tkinter.constants import LEFT, RIGHT, TOP


class NodeContainer:
    def __init__(self, root):
        self.root = root

        node1_frame = Frame(root)
        node1_frame.pack(side=TOP)

        node1_name = Label(node1_frame, text="Node 1 (ttyACM0)")
        node1_name.pack(side=LEFT, padx=10)

        node1_status = Label(node1_frame, text="Status: Running")
        node1_status.pack(side=RIGHT, padx=10)

        node2_frame = Frame(root)
        node2_frame.pack(side=TOP)

        node2_name = Label(node2_frame, text="Node 2 (ttyACM1)")
        node2_name.pack(side=LEFT, padx=10)

        node2_status = Label(node2_frame, text="Status: Running")
        node2_status.pack(side=RIGHT, padx=10)
