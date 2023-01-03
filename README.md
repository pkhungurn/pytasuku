# pytasuku

`pytasuku` is a task execution system implemented in Python. Think of it as a tool similar to GNU Make but you have to implement the command line interface yourself.

## Requirements

The code should work with Python version 3.8 or later. The UI is implemented with [`tkinter`](https://docs.python.org/3/library/tkinter.html), which should come automatically with your Python distribution.

## Installation

You can just copy the `src/pytasuku` to your source code repository, or you can also install it with the following tools.

### Pip

```
pip install git+http://github.com/pkhungurn/pytasuku.git
```

### Poetry

```
poetry add git+http://github.com/pkhungurn/pytasuku.git
```

## What does it do?

`tasuku` allows you to define "tasks." A **task** is a piece of computation that you want to run like like compiling some code, linking some programs, creating/removing files, and so on. A task can be dependent on other tasks, which means that the dependent task can only be executed only after all of its dependencies have been executed. In this way, you can create a dependency graph between tasks in which tasks are vertices, and you draw a directed edge from a dependency to each task that depends on it. `tasuku` ensures that the graph is well formed; that is, the graph has no loops. When you use `tasuku` to execute a task, it takes care to traverse the dependency graph and execute tasks in the right topological order.

### Types of Tasks

Similar to Make, there two main types of tasks.

1. A **command tasks** is a task that is always executed when invoked or when one of its dependencies need to be executed.
2. A **file tasks** is a task that produces a file. It is executed if (1) the output file does not exist, (2) the output file's timestamp is older than one of its (transitive) dependency file tasks, or (3) one of its dependency was invoked. The idea is that a file task is only executed when it is needed to be updated.

It is not advisable to make a file task dependent on a command task because the file task will be always be executed regardless of the file's timestamp.

### Task Names

A task name is similar to a path name of files. The path is always relative to the current directory. For example, you can have

* `a.txt`
* `b/c.txt`
* `b/d/e.txt`
* `b/create_all`
* `b/remove_all`

The first three tasks are supposed to be file tasks (which generally take the name of their output files), and the last two command tasks. We can see that tasks can form directory structures like files, and this is a nice way to organize tasks when there's a mixture of file and command tasks.

### Task-Picking UI

Executing a tasks requires you to know its name. Remembering a task's name when you have create several tens of them can be daunting. `tasuku` comes with a UI that helps you navigate the task directory structure in order to pick one task to execute.

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

## Why `tasuku`?

`tasuku` is one of my self-created software libraries that I always rely on when I have to manage multi-step computation. As an example, in machine learning research, your workflow might look like the following.

1. Download some raw data from the web.
1. Split the data into training, validation, and test datasets.
1. Train ML models on the training dataset with under several hyperparameter settings.
1. Evaluate the models using the validation dataset.
1. Pick the best model according to some metrics.
1. Evaluate the best model using the test dataset.

You can see that each step (except for the first one) depends on those that come before it. Moreover, some of the steps (like Step 3) can take a very long time to complete.

It does not make sense to implement the steps in a single program that runs them sequentially. Some of the steps can fail (e.g., because of bugs in your code, or because a blackout while you are training your models), and you might want to retry them again. A sequential program would redo everything from scratch, not just the only parts that you want to retry. `tasuku` allows you to take advantage of "cached" results, pretty much like Make would only build only parts of a program that need to be changed when you modify a source file.

I created `tasuku` instead of using other build tools such as Make, [Rake](https://ruby.github.io/rake/), [Gradle](https://gradle.org/), or [Bazel](https://bazel.build/) because I would like to have more control on the system. This gives me freedom to define what tasks are, dicate the format or task names, and build the task-picking UI without having to study existing systems in details.

## Release History

* [2022/01/03] v0.1.0: First release.