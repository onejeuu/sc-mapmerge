from pathlib import Path

from scmapmerge import exceptions as exc
from scmapmerge.consts import MapFile
from scmapmerge.datatype import Region


class RegionFile:
    def __init__(self, path: Path):
        self.path = path

        coords = self._parse_filename()

        if not coords.count(MapFile.DELIMITER) == 1:
            raise exc.InvalidRegionFilename(path)

        x, z = coords.split(MapFile.DELIMITER)

        if not self._is_valid_coords(x, z):
            raise exc.InvalidRegionFilename(path)

        self.region = Region(int(x), int(z))

    @property
    def x(self) -> int:
        return self.region.x

    @property
    def z(self) -> int:
        return self.region.z

    @property
    def filesize(self) -> int:
        """Filesize in bytes."""
        return self.path.stat().st_size

    def get_new_filename(self, suffix: str) -> str:
        """Filename with new suffix."""
        return self.path.with_suffix(suffix).name

    def _parse_filename(self) -> str:
        """Replaces invalid delimiters and removes prefix."""
        filename = self.path.stem
        filename = filename.replace("_", MapFile.DELIMITER)
        filename = filename.lstrip(MapFile.PREFIX).lstrip(MapFile.DELIMITER)
        return filename

    def _is_valid_coords(self, *values: str) -> bool:
        """Validates that all passed strings is digits."""
        return all(value.lstrip("-").isdigit() for value in values)

    def __str__(self):
        return f"{self.region}"

    def __repr__(self):
        return str(self)
