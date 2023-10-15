from pathlib import Path

from mapmerge.consts import Folder, MIN_FILESIZE


class Workspace:
    def __init__(self):
        self.folders = [
            Folder.WORKSPACE,
            Folder.CONVERTED,
            Folder.ORIGINAL,
            Folder.OUTPUT
        ]

    def prepare(self):
        if not self.exists:
            self.create_all()

    @property
    def exists(self) -> bool:
        return Folder.WORKSPACE.exists()

    def is_empty(self, folder: Path) -> bool:
        return not any(self.files(folder))

    def create_all(self):
        for folder in self.folders:
            folder.mkdir(parents=True, exist_ok=True)

    def clear(self, folder: Path):
        for entry in self.files(folder):
            entry.unlink(missing_ok=True)

    def clear_all(self):
        for folder in self.folders:
            self.clear(folder)

    def files(self, folder: Path):
        return (entry for entry in folder.iterdir() if entry.is_file())

    def contains_empty_maps(self):
        return any(entry.is_file() and entry.stat().st_size < MIN_FILESIZE for entry in self.ol_files)

    @property
    def ol_files(self):
        return [f for f in self.files(Folder.ORIGINAL) if f.suffix == '.ol']

    @property
    def ol_files_not_empty(self):
        return [f for f in self.ol_files if f.stat().st_size > MIN_FILESIZE]

    @property
    def dds_files(self):
        return [f for f in self.files(Folder.CONVERTED) if f.suffix == '.dds']
