from pathlib import Path
from typing import List

from PIL import Image

from scmapmerge import exceptions as exc
from scmapmerge.datatype import ImgSize, Region
from scmapmerge.consts import MapFile


class RegionFile:
    def __init__(self, path: Path):
        self.path = path

        coords = self._parse_filename()

        if not coords.count(".") == 1:
            raise exc.InvalidRegionFilename(path)

        x, z = coords.split(".")

        if not self._is_valid_coords(x, z):
            raise exc.InvalidRegionFilename(path)

        # TODO: improve: rename for no confusion
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

    def _parse_filename(self):
        return self.path.stem.replace("_", ".").lstrip(MapFile.PREFIX)

    def _is_valid_coords(self, *values: str):
        return all(value.lstrip("-").isdigit() for value in values)

    def __str__(self):
        return f"{self.region}"

    def __repr__(self):
        return str(self)


class RegionsList(List[RegionFile]):
    @classmethod
    def from_pathes(cls, pathes: list[Path]):
        return cls([RegionFile(path) for path in pathes])


class EncryptedRegions(RegionsList):
    # TODO: improve: this is awful

    def contains_empty(self) -> bool:
        return any(
            region.filesize < MapFile.MINIMUM_SIZE
            for region in self
        )

    def filter_empty(self):
        return EncryptedRegions(
            list(filter(lambda region: region.filesize > MapFile.MINIMUM_SIZE, self))
        )

    def contains_preset(self, preset_regions: list[Region]) -> bool:
        # TODO: improve: make it more readable
        r1 = set(region.region for region in self)
        r2 = set(preset_regions)
        return r2.issubset(r1)

    def filter_preset(self, preset_regions: list[Region]):
        return EncryptedRegions(
            list(filter(lambda region: region.region in preset_regions, self))
        )


class ConvertedRegions(RegionsList):
    # TODO: improve: this too

    DEFAULT_SCALE = 512

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
    def scale(self):
        return self._scale or self.DEFAULT_SCALE

    @property
    def width(self) -> int:
        return (abs(self.max_x - self.min_x) + 1) * self.scale

    @property
    def height(self) -> int:
        return (abs(self.max_z - self.min_z) + 1) * self.scale

    def find_scale(self) -> int:
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
        self._scale = size.w
        return self._scale
