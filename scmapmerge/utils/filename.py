import os
from datetime import datetime
from pathlib import Path
from typing import TypeAlias


PathLike: TypeAlias = str | os.PathLike[str] | Path


class FileName:
    START_COUNT = 1

    def __init__(self, base_path: PathLike, template: str, suffix: str, overwrite: bool):
        self.base_path = base_path
        self.template = template
        self.suffix = suffix
        self.overwrite = overwrite

        self.count = self.START_COUNT

    @property
    def path(self) -> Path:
        """Complete file path with count and suffix."""
        return Path(self.base_path, f"{self.filename}.{self.suffix}")

    @property
    def filename(self):
        """Formatted filename with count."""
        if self.count <= self.START_COUNT:
            return self.template
        return f"{self.template} ({self.count})"

    def _parse_datetime(self) -> None:
        """Parses current datetime and updates template."""
        now = datetime.now()
        self.template = now.strftime(self.template)

    def _check_uniqueness(self) -> None:
        """Validates that filename is unique. Increments count."""
        if not self.overwrite:
            while self.path.exists():
                self.count += 1

    def as_path(self) -> Path:
        """Generates complete path. Parsing datetime and check uniqueness."""
        self._parse_datetime()
        self._check_uniqueness()
        return self.path

    def __str__(self):
        return str(self.path.as_posix())

    def __repr__(self):
        return str(self)
