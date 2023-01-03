import logging

from example import tasks
from pytasuku import Workspace
from pytasuku.task_selector_ui import run_task_selector_ui

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    workspace = Workspace()
    tasks.define_tasks(workspace)
    run_task_selector_ui(workspace)
