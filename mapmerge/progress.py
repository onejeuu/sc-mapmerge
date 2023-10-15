from rich import progress
from typing import NamedTuple

from mapmerge.consts import Prefix


class Description(NamedTuple):
    TASK = f"{Prefix.PROGRESS} [b deep_pink2]Wait[/]"
    DONE = f"{Prefix.DONE} [b yellow4]Done[/]"


class FilesProgress:
    def __init__(self, total: int):
        self.progress = progress.Progress(*self.columns)
        self.task_id = self.progress.add_task(Description.TASK, total=total)
        self.progress.start()

    @property
    def columns(self):
        return (
            progress.TextColumn("[progress.description]{task.description}"),
            progress.BarColumn(),
            progress.MofNCompleteColumn(),
            progress.TaskProgressColumn()
        )

    def increment(self):
        self.progress.advance(self.task_id, 1)

    def done(self):
        self.progress.update(self.task_id, description=Description.DONE)
        self.progress.stop()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.done()
