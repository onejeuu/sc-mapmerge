from pathlib import Path

from scmapmerge.exceptions import ScMapMergeException


class WorkspaceError(ScMapMergeException):
    pass


class DirIsEmpty(WorkspaceError):
    def __init__(self, path: Path, hint: str):
        self.path = path
        self.hint = hint

    def __str__(self):
        return f"'{self.path.as_posix()}' has no required files. {self.hint}"


class AssetsPathNotFound(WorkspaceError):
    def __str__(self):
        return "Path to game assets not found."
