from tkinter import Frame, Label
from tkinter.constants import LEFT, RIGHT, TOP, BOTTOM
from typing import Optional


class NodeFrame(Frame):
    STATUS_PREFIX: str = "Status:"

    def __init__(self, node_id: int, available_memory: int, master=None, **kwargs):
        super().__init__(master, cnf={}, **kwargs)
        self.node_id = node_id

        self.node_params_label = Label(self,
                                       text=f"Node id: {node_id}\t"
                                            f"Available memory: {self._get_available_memory_string(available_memory)} KB\t")
        self.node_params_label.pack(side=LEFT)

        self.node_status_label = Label(self, text=f"\t{NodeFrame.STATUS_PREFIX} Free")
        self.node_status_label.pack(side=RIGHT)

        self.node_running_script = Label(self, text='')
        self.node_running_script.pack(side=BOTTOM)

    def update_node_params(self, status: str, available_memory: int, script_txt: Optional[str]):
        self.node_params_label.config(text=f"Node id: {self.node_id}\t"
                                           f"Available memory: {self._get_available_memory_string(available_memory)} KB\t")
        self.node_status_label.config(text=NodeFrame.STATUS_PREFIX + status)

        if script_txt is not None:
            self.node_running_script.config(text=script_txt)

    def _get_available_memory_string(self, memory: int) -> str:
        available_memory_kb = memory / 1000
        if memory % 1000 == 0:
            return '{:.0f}'.format(available_memory_kb)
        else:
            return '{:.1f}'.format(available_memory_kb)


class NodeContainer:
    def __init__(self, root):
        self.root = root

        self.node_frames: dict[int, NodeFrame] = dict()
        self.node_container_frame = Frame(self.root)
        self.node_container_frame.pack()

    def add_node_entry(self, node_id: int, available_memory: int, supported_features: int) -> None:
        # TODO: Supported features not showing
        new_node_frame = NodeFrame(master=self.node_container_frame,
                                   node_id=node_id,
                                   available_memory=available_memory,
                                   height=200,
                                   borderwidth=2,
                                   relief="groove")
        new_node_frame.pack(side=TOP)
        self.node_frames[node_id] = new_node_frame

    def edit_node_entry(self, node_id: int, status: str, available_memory: int, script_txt: Optional[str]):
        # TODO: Supported features not showing
        node_frame = self.node_frames.get(node_id)
        node_frame.update_node_params(status, available_memory, script_txt)
