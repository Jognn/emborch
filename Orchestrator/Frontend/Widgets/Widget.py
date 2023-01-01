class Widget:
    def __init__(self, master):
        self.master = master
        self.items = list()
        
    def show_items(self):
        for item in self.items:
            item.pack()
