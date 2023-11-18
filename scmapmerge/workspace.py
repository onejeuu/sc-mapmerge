from datetime import datetime
from pathlib import Path

from scmapmerge.consts import MINIMUM_MAP_FILE_SIZE, Folder


class Workspace:
    def __init__(self, filename: str):
        self.filename = filename

        self.folders = [
            Folder.WORKSPACE,
            Folder.ENCRYPTED,
            Folder.CONVERTED,
            Folder.OUTPUT
        ]

    @property
    def exists(self) -> bool:
        return Folder.WORKSPACE.exists()

    def is_empty(self, folder: Path) -> bool:
        return not any(self.files(folder))

    def create_all(self) -> None:
        for folder in self.folders:
            folder.mkdir(parents=True, exist_ok=True)

    def clear(self, folder: Path) -> None:
        for entry in self.files(folder):
            entry.unlink(missing_ok=True)

    def clear_all(self) -> None:
        for folder in self.folders:
            self.clear(folder)

    def files(self, folder: Path) -> list[Path]:
        return [entry for entry in folder.iterdir() if entry.is_file()]

    def contains_empty_maps(self) -> bool:
        return any(entry.is_file() and entry.stat().st_size < MINIMUM_MAP_FILE_SIZE for entry in self.ol_files)

    @property
    def ol_files(self) -> list[Path]:
        return [f for f in self.files(Folder.ENCRYPTED) if f.suffix == '.ol']

    @property
    def dds_files(self) -> list[Path]:
        return [f for f in self.files(Folder.CONVERTED) if f.suffix == '.dds']

    @property
    def not_empty_ol_files(self) -> list[Path]:
        return [f for f in self.ol_files if f.stat().st_size > MINIMUM_MAP_FILE_SIZE]

    def get_output_image_path(self) -> Path:
        folder = Path(Folder.OUTPUT)
        current = datetime.now()
        date = current.strftime("%Y.%m.%d")

        filename = f"{self.filename} {date}.png"
        path = folder / filename

        # Uniqueness check
        count = 2
        while path.exists():
            filename = f"{self.filename} {date} ({count}).png"
            path = folder / filename
            count += 1

        return path
