from pathlib import Path


class Region:
    def __init__(self, path: Path):
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
    def __init__(self, *regions: Region):
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

    def sort(self, key=lambda region: (region.x, region.z), *args, **kwargs):
        super().sort(key=key, *args, **kwargs)

    def __repr__(self):
        return f"<RegionsList> {self.min_x=} {self.min_z=} {self.max_x=} {self.max_z=}"
