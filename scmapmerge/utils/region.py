from pathlib import Path

from PIL import Image

from scmapmerge import exceptions as exc
from scmapmerge.datatype import ImgSize


class Region:
    PREFIX = "r."

    def __init__(self, path: Path):
        self.path = path

        if not self.validate_name():
            raise exc.InvalidRegionFilename(path)

        self._x, self._z = self.coords.split(".")

        if not self.validate_coords():
            raise exc.InvalidRegionFilename(path)

    @property
    def coords(self):
        return self.path.stem.lstrip(self.PREFIX)

    def validate_name(self) -> bool:
        return self.coords.count(".") == 1

    def validate_coords(self) -> bool:
        x = self._x.lstrip("-")
        z = self._z.lstrip("-")
        return x.isdigit() and z.isdigit()

    @property
    def x(self) -> int:
        return int(self._x)

    @property
    def z(self) -> int:
        return int(self._z)

    def __str__(self):
        return f"<Region> {self.x=} {self.z=}"

    def __repr__(self):
        return str(self)


class RegionsList(list):
    def __init__(self, regions: list[Region]):
        super().__init__(regions)
        self.scale = self._get_scale()

    @property
    def min_x(self) -> int:
        return min(region.x for region in self)

    @property
    def min_z(self) -> int:
        return min(region.z for region in self)

    @property
    def max_x(self) -> int:
        return max(region.x for region in self)

    @property
    def max_z(self) -> int:
        return max(region.z for region in self)

    @property
    def width(self) -> int:
        return (abs(self.max_x - self.min_x) + 1) * self.scale

    @property
    def height(self) -> int:
        return (abs(self.max_z - self.min_z) + 1) * self.scale

    def _get_scale(self) -> int:
        sizes: set[ImgSize] = set()

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
