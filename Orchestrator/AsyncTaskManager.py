import asyncio
from typing import Coroutine


class AsyncTaskManager:
    def __init__(self, task_group: asyncio.TaskGroup):
        self._running_tasks: set[asyncio.Task] = set()
        self._task_group: asyncio.TaskGroup = task_group

    def add_task(self, coroutine: Coroutine) -> None:
        new_task = self._task_group.create_task(coroutine)
        self._running_tasks.add(new_task)

    def stop_all_tasks(self) -> None:
        for task in self._running_tasks:
            task.cancel()
