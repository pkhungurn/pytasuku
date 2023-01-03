from typing import List, Iterable

from pytasuku import Workspace
from pytasuku.indexed.indexed_tasks import IndexedTasks
from pytasuku.indexed.no_index_command_tasks import NoIndexCommandTasks


class AllTasks(NoIndexCommandTasks):
    def __init__(
            self,
            workspace: Workspace, prefix: str,
            tasks: Iterable[IndexedTasks],
            command_name: str = "all",
            define_tasks_immediately: bool = True):
        super().__init__(workspace, prefix, command_name, define_tasks_immediately)
        self.tasks = [t for t in tasks]
        if define_tasks_immediately:
            self.define_tasks()

    def execute_run_command(self):
        for task in self.tasks:
            self.workspace.run(task.run_command)

    def execute_clean_command(self):
        for task in self.tasks:
            self.workspace.run(task.clean_command)