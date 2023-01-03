import os
import random

from pytasuku import Workspace, file_task, command_task


def define_tasks(workspace: Workspace):
    a_file_name = "data/a.txt"

    @file_task(workspace, a_file_name, [])
    def create_a_file():
        os.makedirs(os.path.dirname(a_file_name), exist_ok=True)
        with open(a_file_name, "wt") as fout:
            fout.write("%d\n" % random.randint(0, 100))

    c_file_name = "data/b/c.txt"

    @file_task(workspace, c_file_name, [a_file_name])
    def create_c_file():
        with open(a_file_name, "rt") as fin:
            lines = fin.readlines()
            number = int(lines[0])
        os.makedirs(os.path.dirname(c_file_name), exist_ok=True)
        with open(c_file_name, "wt") as fout:
            fout.write("%d\n" % (number * 2))

    e_file_name = "data/b/d/e.txt"

    @file_task(workspace, e_file_name, [a_file_name, c_file_name])
    def create_e_file():
        with open(a_file_name, "rt") as fin:
            lines = fin.readlines()
            a_number = int(lines[0])
        with open(c_file_name, "rt") as fin:
            lines = fin.readlines()
            c_number = int(lines[0])
        os.makedirs(os.path.dirname(e_file_name), exist_ok=True)
        with open(e_file_name, "wt") as fout:
            fout.write("%d\n" % (a_number + c_number))

    @command_task(workspace, "data/create_all", [a_file_name, c_file_name, e_file_name])
    def create_all_files():
        print("Running all tasks!!!")

    @command_task(workspace, "data/delete_all", [])
    def delete_all_files():
        for file_name in [a_file_name, c_file_name, e_file_name]:
            if os.path.exists(file_name):
                os.remove(file_name)
                print(f"Deleted {file_name}")