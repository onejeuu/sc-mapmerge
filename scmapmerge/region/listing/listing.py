from pathlib import Path
from typing import Callable, Literal, Optional, Self

from scmapmerge.region.file import RegionFile


class RegionsListing:
    def __init__(self, regions: Optional[list[RegionFile]] = None):
        self.regions: list[RegionFile] = regions or []

    @classmethod
    def from_paths(cls, paths: list[Path]) -> Self:
        return cls([RegionFile(path) for path in paths])

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
    def new_suffix(self) -> Literal[".png", ".dds"]:
        match self.suffix:
            case ".mic":
                return ".png"

            case ".ol" | _:
                return ".dds"

    def filter(self, func: Callable[[RegionFile], bool]):
        self.regions = list(filter(func, self.regions))

    def __len__(self):
        return len(self.regions)

    def __iter__(self):
        return iter(self.regions)
