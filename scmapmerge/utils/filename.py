import os
from datetime import datetime
from pathlib import Path
from typing import TypeAlias


PathLike: TypeAlias = str | os.PathLike[str] | Path


class FileName:
    def __init__(self, base_path: PathLike, template: str):
        self.base_path = base_path
        self.filename = template

    @property
    def path(self):
        return Path(self.base_path, self.filename)

    def _parse_datetime(self):
        now = datetime.now()
        self.filename = now.strftime(self.filename)

    def _check_uniqueness(self):
        count = 2

        while self.path.exists():
            self.filename = f"{self.filename} ({count})"
            count += 1

    def as_path(self) -> Path:
        self._parse_datetime()
        self._check_uniqueness()
        return self.path

    def __str__(self):
        return str(self.path.as_posix())

    def __repr__(self):
        return str(self)
