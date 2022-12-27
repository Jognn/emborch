import asyncio
from tkinter import Tk


class AsyncTk(Tk):
    "Basic Tk with an asyncio-compatible event loop"

    def __init__(self):
        super().__init__()
        self.running = True
        self.runners = [self.tk_loop()]

    async def tk_loop(self):
        "asyncio 'compatible' tk event loop?"
        while self.running:
            self.update()
            await asyncio.sleep(0.05)

    def stop(self):
        self.running = False

    async def run(self):
        await asyncio.gather(*self.runners)
