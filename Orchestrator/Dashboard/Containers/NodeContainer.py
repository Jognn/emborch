from tkinter import Frame, Label
from tkinter.constants import LEFT, RIGHT, TOP


class NodeFrame(Frame):
    STATUS_PREFIX: str = "Status:"

    def __init__(self, node_id: int, available_memory: int, master=None, **kwargs):
        super().__init__(master, cnf={}, **kwargs)
        self.node_id = node_id
        self.available_memory = available_memory

        self.node_params_label = Label(self,
                                       text=f"Node id: {node_id}\t"
                                            f"Available memory: {self._get_available_memory_string()} KB\t")
        self.node_params_label.pack(side=LEFT)

        self.node_status_label = Label(self, text=f"\t{NodeFrame.STATUS_PREFIX} Free")
        self.node_status_label.pack(side=RIGHT)

    def change_status(self, new_status: str):
        self.node_status_label.config(text=NodeFrame.STATUS_PREFIX + new_status)

    def _get_available_memory_string(self) -> str:
        available_memory_kb = self.available_memory / 1000
        if self.available_memory % 1000 == 0:
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
        new_node_frame = NodeFrame(master=self.node_container_frame, node_id=node_id, available_memory=available_memory)
        new_node_frame.pack(side=TOP)
        self.node_frames[node_id] = new_node_frame

    def node_entry_running(self, node_id: int, available_memory: int, script_txt: str) -> None:
        pass
