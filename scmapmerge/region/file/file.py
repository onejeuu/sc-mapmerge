from pathlib import Path

from scmapmerge.region.exceptions import InvalidRegionFilename
from scmapmerge.consts import MapFile
from scmapmerge.datatype import Region

from .base import BaseRegionFile


class RegionFile(BaseRegionFile):
    def __init__(self, path: Path):
        self.path = path

        coords = self._parse_filename()

        if not coords.count(MapFile.DELIMITER) == 1:
            raise InvalidRegionFilename(path)

        x, z = coords.split(MapFile.DELIMITER)

        if not self._is_valid_coords(x, z):
            raise InvalidRegionFilename(path)

        self.region = Region(int(x), int(z))

    @property
    def x(self) -> int:
        return self.region.x

    @property
    def z(self) -> int:
        return self.region.z

    @property
    def filesize(self) -> int:
        return self.path.stat().st_size

    @property
    def is_empty(self):
        return self.filesize <= MapFile.MINIMUM_SIZE

    def get_new_filename(self, suffix: str) -> str:
        return self.path.with_suffix(suffix).name

    def _parse_filename(self) -> str:
        filename = self.path.stem
        filename = filename.replace("_", MapFile.DELIMITER)
        filename = filename.lstrip(MapFile.PREFIX).lstrip(MapFile.DELIMITER)
        return filename

    def _is_valid_coords(self, *values: str) -> bool:
        return all(value.lstrip("-").isdigit() for value in values)

    def __str__(self):
        return f"{self.region}"

    def __repr__(self):
        return str(self)
