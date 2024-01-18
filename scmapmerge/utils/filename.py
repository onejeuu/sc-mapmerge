import os
from datetime import datetime
from pathlib import Path
from typing import TypeAlias


PathLike: TypeAlias = str | os.PathLike[str] | Path


class FileName:
    DEFAULT_COUNT = 2

    def __init__(self, base_path: PathLike, template: str, suffix: str, overwrite: bool):
        self.base_path = base_path
        self.filename = template
        self.suffix = suffix
        self.overwrite = overwrite

        self.count = self.DEFAULT_COUNT

    @property
    def path(self) -> Path:
        return Path(self.base_path, f"{self.filename}.{self.suffix}")

    def _parse_datetime(self) -> None:
        now = datetime.now()
        self.filename = now.strftime(self.filename)

    def _check_uniqueness(self) -> None:
        if not self.overwrite:
            while self.path.exists():
                # removing previous count
                self.filename = self.filename.rstrip(f" ({self.count - 1})")

                self.filename += f" ({self.count})"
                self.count += 1

    def as_path(self) -> Path:
        self._parse_datetime()
        self._check_uniqueness()
        return self.path

    def __str__(self):
        return str(self.path.as_posix())

    def __repr__(self):
        return str(self)
