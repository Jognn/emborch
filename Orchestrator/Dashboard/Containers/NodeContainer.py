from typing import Optional

import ttkbootstrap as ttk


class NodeDataEntry:

    def __init__(self, treeview: ttk.Treeview, state: str, node_id: int, name: str, max_memory: int):
        self._treeview_ref: ttk.Treeview = treeview
        self.node_id: int = node_id

        self.state: str = state
        self.name: str = name
        self.max_memory: int = max_memory
        self.available_memory: int = max_memory
        self.script_txt: Optional[str] = None

        memory_text = f"{self._format_memory(self.available_memory)} / {self._format_memory(self.max_memory)} KB"
        self._treeview_ref.insert(parent='',
                                  index='end',
                                  iid=str(self.node_id),
                                  values=(self.state, self.node_id, self.name, memory_text))

    def update_node_entry(self) -> None:
        self._treeview_ref.set(str(self.node_id), "state", self.state)
        self._treeview_ref.set(str(self.node_id), "memory", self._get_memory_string())

    def _get_memory_string(self) -> str:
        return f"{self._format_memory(self.available_memory)} / {self._format_memory(self.max_memory)} KB"

    def _format_memory(self, memory: int) -> str:
        available_memory_kb = memory / 1000
        if memory % 1000 == 0:
            return '{:.0f}'.format(available_memory_kb)
        else:
            return '{:.1f}'.format(available_memory_kb)


class NodeContainer:
    def __init__(self, root):
        self.root = root
        self.node_data_entries: dict[int, NodeDataEntry] = dict()

        self.node_container_frame = ttk.Frame(self.root)
        self.node_container_frame.pack()

        treeview_style = ttk.Style()
        treeview_style.configure('Treeview', rowheight=40)
        treeview_style.configure('Treeview.Heading', background="lightblue")

        self.treeview = ttk.Treeview(self.node_container_frame,
                                     columns=("state", "id", "name", "memory"),
                                     show='headings',
                                     height=5)

        self.treeview.column("state", anchor=ttk.CENTER, width=110, minwidth=0)
        self.treeview.column("id", anchor=ttk.CENTER, width=80, minwidth=0)
        self.treeview.column("name", anchor=ttk.CENTER, width=160, minwidth=0)
        self.treeview.column("memory", anchor=ttk.CENTER, width=160, minwidth=0)

        self.treeview.heading("state", text="Status")
        self.treeview.heading("id", text="Id")
        self.treeview.heading("name", text="Name")
        self.treeview.heading("memory", text="Available memory")

        self.treeview.pack(pady=10)

    def add_node_entry(self, node_id: int, name: str, state: str, available_memory: int,
                       supported_features: int) -> None:
        # TODO: Supported features not showing
        new_node_data_entry = NodeDataEntry(self.treeview,
                                            state=state,
                                            node_id=node_id,
                                            name=name,
                                            max_memory=available_memory)
        self.node_data_entries[node_id] = new_node_data_entry

    def edit_node_entry(self, node_id: int, state: str, available_memory: int, script_txt: Optional[str]):
        # TODO: Supported features not showing
        node_data_entry = self.node_data_entries[node_id]
        node_data_entry.state = state
        node_data_entry.available_memory = available_memory
        node_data_entry.script_txt = script_txt

        node_data_entry.update_node_entry()
