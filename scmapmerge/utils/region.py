from pathlib import Path
from typing import Callable, Optional

from PIL import Image
from scfile.enums import FileSuffix

from scmapmerge import exceptions as exc
from scmapmerge.consts import MapFile
from scmapmerge.datatype import Box, ImgCoords, ImgSize, Region
from scmapmerge.utils.presets import BasePreset


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


class RegionsList:
    def __init__(self, regions: Optional[list[RegionFile]] = None):
        self.regions: list[RegionFile] = regions or []

    @property
    def x(self) -> list[int]:
        return list(r.x for r in self.regions)

    @property
    def z(self) -> list[int]:
        return list(r.z for r in self.regions)

    @property
    def suffix(self) -> str:
        if len(self.regions) > 0:
            region = self.regions[0]
            return region.path.suffix
        return ""

    @property
    def new_suffix(self) -> str:
        # TODO: improve: its still bad

        old_suffix = FileSuffix(self.suffix.lstrip("."))
        new_suffix = FileSuffix.DDS

        if old_suffix == FileSuffix.MIC:
            new_suffix = FileSuffix.PNG

        return f".{new_suffix}"

    @classmethod
    def from_pathes(cls, pathes: list[Path]):
        return cls(
            [RegionFile(path) for path in pathes]
        )

    def filter(self, func: Callable):
        self.regions = list(filter(func, self.regions))

    def __len__(self):
        return len(self.regions)

    def __iter__(self):
        return iter(self.regions)


class EncryptedRegions(RegionsList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.preset: Optional[type[BasePreset]] = None

    @property
    def preset_regions(self) -> list[Region]:
        if self.preset:
            return self.preset.regions
        return []

    def contains_empty(self) -> bool:
        return any(
            r.filesize <= MapFile.MINIMUM_SIZE
            for r in self.regions
        )

    def filter_empty(self):
        self.filter(
            lambda r: r.filesize > MapFile.MINIMUM_SIZE and r.region not in self.preset_regions
        )

    def filter_preset(self):
        self.filter(
            lambda r: r.region in self.preset_regions
        )

    @property
    def regions_set(self) -> set[Region]:
        return set(r.region for r in self.regions)

    @property
    def contains_preset(self) -> bool:
        return self.regions_set.issuperset(self.preset_regions)

    @property
    def missing_preset_regions(self) -> set:
        return set(self.preset_regions) - self.regions_set

    def __str__(self):
        return str(self.regions)


class ConvertedRegions(RegionsList):
    DEFAULT_SCALE = 512

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale: int = self.DEFAULT_SCALE

    @property
    def bounds(self) -> Box:
        if not self.regions:
            return Box(0, 0, 0, 0)

        x = list(r.x for r in self.regions)
        z = list(r.z for r in self.regions)

        return Box(min(x), min(z), max(x), max(z))

    @property
    def size(self) -> ImgSize:
        width = self.scale * (abs(self.bounds.left - self.bounds.right) + 1)
        height = self.scale * (abs(self.bounds.top - self.bounds.bottom) + 1)

        return ImgSize(width, height)

    def region_to_xy(self, region: RegionFile) -> ImgCoords:
        x = region.x - self.bounds.left
        y = region.z - self.bounds.top

        return ImgCoords(x * self.scale, y * self.scale)

    def find_scale(self) -> int:
        sizes: set[ImgSize] = set()

        # Check that all images are square
        for region in self.regions:
            with Image.open(region.path) as img:
                size = ImgSize(*img.size)

                if size.w != size.h:
                    raise exc.ImageIsNotSquare(size)

                sizes.add(size)

        # Check that all images have the same resolution
        if len(sizes) != 1:
            raise exc.ImagesSizesNotSame(sizes)

        size = sizes.pop()
        self.scale = size.w
        return self.scale
