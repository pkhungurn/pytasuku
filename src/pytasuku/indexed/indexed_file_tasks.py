import abc
from typing import List

from pytasuku import Workspace
from pytasuku.indexed.indexed_tasks import IndexedTasks


class IndexedFileTasks(IndexedTasks, abc.ABC):
    def __init__(self, workspace: Workspace, prefix: str):
        super().__init__(workspace, prefix)

    @property
    @abc.abstractmethod
    def file_list(self) -> List[str]:
        pass

    @abc.abstractmethod
    def get_file_name(self, *indices: int) -> str:
        pass
