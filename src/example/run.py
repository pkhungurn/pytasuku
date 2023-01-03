import os
import sys
import logging

from example import tasks
from pytasuku import *

def replace_sep_with_slash(path):
    comps = path.split(os.path.sep)
    return "/".join(comps)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python src/example/run.py <task-name-1> <task-name-2> ...")
        sys.exit(0)

    logging.basicConfig(level=logging.INFO)
    workspace = Workspace()
    tasks.define_tasks(workspace)

    with workspace.session():
        for arg in sys.argv[1:]:
            arg = replace_sep_with_slash(arg)
            workspace.run(arg)