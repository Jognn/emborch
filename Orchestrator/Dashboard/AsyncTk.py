import asyncio
import logging
from tkinter import Tk

from Orchestrator.AsyncTaskManager import AsyncTaskManager


class AsyncTk(Tk):
    """ Basic Tk with an asyncio-compatible event loop """

    def __init__(self, async_task_manager: AsyncTaskManager):
        super().__init__()
        self.async_task_manager = async_task_manager
        self.async_task_manager.add_task(self.run())

    def destroy(self) -> None:
        super().destroy()
        self.async_task_manager.stop_all_tasks()
        logging.info("Emborch has stopped working!")

    async def run(self) -> None:
        while True:
            self.update()
            await asyncio.sleep(0)
