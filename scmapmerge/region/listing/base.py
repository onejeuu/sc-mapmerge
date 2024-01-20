from pathlib import Path
from typing import Callable, Literal, Optional

from scmapmerge.region.file import RegionFile


class RegionsList:
    def __init__(self, regions: Optional[list[RegionFile]] = None):
        self.regions: list[RegionFile] = regions or []

    @property
    def x(self) -> list[int]:
        """List of x values."""
        return list(r.x for r in self.regions)

    @property
    def z(self) -> list[int]:
        """List of z values."""
        return list(r.z for r in self.regions)

    @property
    def suffix(self) -> str:
        """Suffix of first map file. Or empty string."""
        if len(self.regions) > 0:
            region = self.regions[0]
            return region.path.suffix
        return ""

    @property
    def new_suffix(self) -> Literal[".png", ".dds"]:
        """New suffix based on old one."""
        match self.suffix:
            case ".mic":
                return ".png"

            case ".ol" | _:
                return ".dds"

    @classmethod
    def from_pathes(cls, pathes: list[Path]):
        """Create instance from list of Path."""
        return cls(
            [RegionFile(path) for path in pathes]
        )

    def filter(self, func: Callable[[RegionFile], bool]):
        """Filter regions items using specified function."""
        self.regions = list(filter(func, self.regions))

    def __len__(self):
        return len(self.regions)

    def __iter__(self):
        return iter(self.regions)
