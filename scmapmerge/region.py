from pathlib import Path

from scmapmerge.exceptions import InvalidRegionFilename


class Region:
    def __init__(self, path: Path):
        if not path.stem.count(".") == 2:
            raise InvalidRegionFilename(path)

        self.path = path
        _, self._x, self._z = path.stem.split(".")

    @property
    def x(self):
        return int(self._x)

    @property
    def z(self):
        return int(self._z)

    def __str__(self):
        return f"<Region> (x={self.x}, z={self.z})"

    def __repr__(self):
        return str(self)


class RegionsList(list):
    def __init__(self, regions: list[Region]):
        super().__init__(regions)

    @property
    def min_x(self):
        return min(region.x for region in self)

    @property
    def min_z(self):
        return min(region.z for region in self)

    @property
    def max_x(self):
        return max(region.x for region in self)

    @property
    def max_z(self):
        return max(region.z for region in self)

    @property
    def width(self):
        return abs(self.max_x - self.min_x)

    @property
    def height(self):
        return abs(self.max_z - self.min_z)

    def sort(self, key=lambda region: (region.x, region.z), reverse: bool = False):
        super().sort(key=key, reverse=reverse)

    def __repr__(self):
        return f"<RegionsList> {self.min_x=} {self.min_z=} {self.max_x=} {self.max_z=}"
