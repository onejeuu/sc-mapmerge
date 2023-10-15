from pathlib import Path

from mapmerge.consts import Folder


class Workspace:
    def __init__(self):
        ...

    def prepare(self):
        if not self.exists:
            self.create_all()

    @property
    def exists(self) -> bool:
        return Folder.WORKSPACE.exists()

    @property
    def full_empty(self):
        for folder in self.temp_folders:
            for _ in self.files(folder):
                return False
        return True

    def is_empty(self, folder: Path):
        for _ in self.files(folder):
            return False
        return True

    def create_all(self):
        for folder in self.folders:
            folder.mkdir(exist_ok=True)

    def clear(self, folder: Path):
        for entry in self.files(folder):
            entry.unlink()

    def clear_all(self):
        for folder in self.temp_folders:
            self.clear(folder)

    def files(self, folder: Path):
        for entry in folder.iterdir():
            if entry.is_file():
                yield entry

    @property
    def ol_files(self):
        return [f for f in self.files(Folder.ORIGINAL) if f.suffix == ".ol"]

    @property
    def dds_files(self):
        return [f for f in self.files(Folder.CONVERTED) if f.suffix == ".dds"]

    @property
    def folders(self):
        return (
            Folder.WORKSPACE,
            Folder.CONVERTED,
            Folder.ORIGINAL,
            Folder.OUTPUT
        )

    @property
    def temp_folders(self):
        return (
            Folder.CONVERTED,
            Folder.ORIGINAL
        )
