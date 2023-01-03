# pytasuku

`pytasuku` is a task execution system implemented in Python. Think of it as a tool similar to GNU Make but you have to implement the command line interface yourself.

## Requirements

The code should work with Python version 3.8 or later. The UI is implemented with [`tkinter`](https://docs.python.org/3/library/tkinter.html), which should come automatically with your Python distribution.

## Installation

You can just copy the `src/pytasuku` to your source code repository, or you can also install it with pip.

### Pip

```
pip install git+http://github.com/pkhungurn/pytasuku.git
```

### Poetry

```
poetry add git+http://github.com/pkhungurn/pytasuku.git
```

## Running the Example

I use [Poetry](https://python-poetry.org/) to maintain dependencies. Follow the instruction [here](https://python-poetry.org/docs/#installation) to install it into your system.

Next, you need to create a Python environment with Python of at least version 3.8. For example, I used [Anaconda](https://www.anaconda.com/) to do the job. After installing Anaconda, I ran the following command in my shell.

```
conda create -n pytasuku python=3.8
```

Then, you can activate the environment by running the command below.

```
conda activate pytasuku
```

Next, clone this repository, and change your working directory to the repo's directory. Invoke Poetry to install the package.

```
poetry intall
```

There's example code in the `src/example` directory. Execute

```
poetry run python src/example/run_ui.py
```

to run the task-picking UI. To execute a task directly, run a command like

```
poetry run python src/example/run.py <task-name>
```

For example, to create all the files prepared as parts the example run:

```
poetry run python src/example/run.py data/create_all
```

To delete all the files to start the process over, run:

```
poetry run python src/example/run.py data/delete_all
```

## Usage Guide

### Step 1: Create a Workspace

A **workspace** is an object that keeps track of tasks and their dependencies. It allows you to execute tasks in the correct topological order. Before you can define any tasks, you need to create an instance of the `Workspace` class.

```python
from pytasuku import Workspace

workspace = Workspace()
```

### Step 2: Define Tasks

A **task** is just a Python function that has no arguments and returns nothing.

#### Command Tasks

A command task can be defined by decorating a function with the `@command_task` decorator. The decorator takes three arguments, in order.

1. A workspace that is going to hold the task.
1. The task name.
1. A list of names of the task's dependencies.

Below, we create two tasks. The second depends on the first.

```python
from pytasuku import command_task

@command_task(workspace, 'task_0', [])
def run_task_0():
  print("Running task_0")


@command_task(workspace, 'task_1', ['task_0'])
def run_task_1():
  print("Running task_1")
```

#### File Tasks

Similarly, a file task can be created using the `@file_task` decorator, and it takes in the same argument as the `@command_task` decorator. One thing to keep in mind is that you are responsible for making sure that the task you define actually the file that is the name of the task. It won't work otherwise.

```python
from pytasuku import file_task

@file_task(workspace, 'a.txt', [])
def create_a_txt():
  with open('a.txt', 'wt') as fout:
    fout.write("AAA")


@file_task(workspace, 'b.txt', ['a.txt'])
def create_b_txt():
  with open('b.txt', 'wt') as fout:
    fout.write("BBB")


@command_task(workspace, 'create_files', ['a.txt', 'b.txt'])
def create_files():
  pass
```

In the above listing, we create two file tasks, `a.txt` and `b.txt`, where the second depends on the first. Note that the functions for these tasks actually write new files whose names are the task names. ***IT IS THE RESPONSIBILITY OF YOU, THE USER, TO DO THIS.*** Lastly, we created a command task that depends on the file tasks. The command task itself does not do anything. However, since it depends on the two file tasks, the system will check whether the files exists and are updated every time you invoke the command task. If not, the files will be created.

### Step 3: Run Task(s) in a Session

To run a task, you need to start a **session**. It is a time period dedicated to running tasks. When you start a session, the system will build a dependency graph of the task, freeze it, and checks whether the graph is well-formed or not. If not, the system will complain and throw an exception. If not you, can run tasks by calling the `run` method of the `Workspace` class.

The `Workspace` class has the `start_session` and `end_session` methods that do what their name say. So, the following snippet to run the `create_files` task we just defined.

```python
workspace.start_session()
workspace.run("create_files")
workspace.end_session()
```

However, there's also the `session` method that can be used with Python's `with` clause. This method is a context manager that starts a session when you enter the method and ends it when you leave.

```python
with workspace.session():
  workspace.run("create_files")
```

After a session ends, you can start creating tasks again.

### Step 4 (Optional): Use the Task Selector UI

If you do not want to specify a task's name programmatically, you can run a task selector UI that allows you to pick a task, and the UI will take care of creating a session and running it. Invoking the UI is very simple, just give the workspace (after you have created all the tasks) to the `run_task_selector_ui` function.

```python
from pytasuku.task_selector_ui import run_task_selector_ui

run_task_selector_ui(workspace)
```

## Code Organization

The `src/example` directory contains an example of how I usually organize my project. It has three main files.

* `src/example/tasks.py` is responsible for defining the tasks, which is done in the `define_tasks` function that takes a `Workspace` as an argument.
* `src/example/run.py` is the command line interface of the system. 
* `src/example/run_ui.py` runs the task selector UI.