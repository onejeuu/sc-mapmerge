from pathlib import Path

from scmapmerge.exceptions import ScMapMergeException


class WorkspaceError(ScMapMergeException):
    pass


class FolderIsEmpty(WorkspaceError):
    def __init__(self, folder: Path, hint: str):
        self.folder = folder
        self.hint = hint

    def __str__(self):
        return f"'{self.folder.as_posix()}' folder has no required files. {self.hint}"


class AssetsPathNotFound(WorkspaceError):
    def __str__(self):
        return "Path to game assets not found."
