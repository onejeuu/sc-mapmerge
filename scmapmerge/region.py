from pathlib import Path

from PIL import Image

from scmapmerge import exceptions as exc
from scmapmerge.utils import ImgSize


class Region:
    def __init__(self, path: Path):
        if not path.stem.count(".") == 2:
            raise exc.InvalidRegionFilename(path)

        self.path = path
        self._prefix, self._x, self._z = path.stem.split(".")

    @property
    def x(self):
        return int(self._x)

    @property
    def z(self):
        return int(self._z)

    def __str__(self):
        return f"<Region> {self.x=} {self.z=}"

    def __repr__(self):
        return str(self)


class RegionsList(list):
    def __init__(self, regions: list[Region]):
        super().__init__(regions)
        self.scale = self.get_scale()

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
        return (abs(self.max_x - self.min_x) + 1) * self.scale

    @property
    def height(self):
        return (abs(self.max_z - self.min_z) + 1) * self.scale

    def sort(self, key=lambda region: (region.x, region.z), reverse: bool = False):
        super().sort(key=key, reverse=reverse)

    def get_scale(self):
        sizes = set()

        # Check that all images are square
        for region in self:
            with Image.open(region.path) as img:
                size = ImgSize(img.width, img.height)

                if size.w != size.h:
                    raise exc.ImageIsNotSquare(size)

                sizes.add(size)

        # Check that all images have the same resolution
        if len(sizes) != 1:
            raise exc.ImagesSizesNotSame(sizes)

        size = sizes.pop()
        return size.w

    def __repr__(self):
        return f"<RegionsList> {self.min_x=} {self.min_z=} {self.max_x=} {self.max_z=}"
