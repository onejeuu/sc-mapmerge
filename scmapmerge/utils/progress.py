from rich import progress
from typing import Optional, Any


class Description:
    WAIT = "⏳ [b deep_pink2]Wait[/]"
    DONE = "✅ [b yellow4]Done[/]"
    ERROR = "❌ [b red3]Error[/]"


class FilesProgress:
    def __init__(self, total: int):
        self.progress = progress.Progress(*self.columns)
        self.task_id = self.progress.add_task(Description.WAIT, total=total)
        self.progress.start()

    @property
    def columns(self):
        return (
            progress.TextColumn("[progress.description]{task.description}"),
            progress.BarColumn(bar_width=25),
            progress.MofNCompleteColumn(),
            progress.TaskProgressColumn()
        )

    def increment(self) -> None:
        self.progress.advance(self.task_id, 1)

    def update_description(self, description: Optional[str] = None) -> None:
        self.progress.update(self.task_id, description=description)

    def done(self) -> None:
        self.update_description(Description.DONE)

    def error(self) -> None:
        self.update_description(Description.ERROR)

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[Any]
    ):
        if exc_type is None:
            self.done()
        else:
            self.error()

        self.progress.stop()
