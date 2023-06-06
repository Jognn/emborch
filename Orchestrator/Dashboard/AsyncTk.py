import asyncio
from tkinter import Tk
from typing import Coroutine


class AsyncTk(Tk):
    """ Basic Tk with an asyncio-compatible event loop """

    def __init__(self, running_tasks: list[Coroutine]):
        super().__init__()
        self.running = False
        self.running_tasks = running_tasks
        self.running_tasks.append(self.tk_loop())

    async def tk_loop(self) -> None:
        """ asyncio 'compatible' tk event loop? """
        while self.running:
            self.update()
            await asyncio.sleep(0)

    def stop(self) -> None:
        self.running = False

    async def run(self) -> None:
        self.running = True
        await asyncio.gather(*self.running_tasks)
