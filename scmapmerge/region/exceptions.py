from pathlib import Path
from scmapmerge.datatype import ImageSize

from scmapmerge.exceptions import ScMapMergeException


class RegionError(ScMapMergeException):
    pass


class InvalidRegionFilename(RegionError):
    def __init__(self, path: Path):
        self.path = path

    def __str__(self):
        return f"Region (map image file) '{self.path.as_posix()}' has invalid filename format."


class RegionScaleError(RegionError):
    pass


class ChunkNotSquare(RegionScaleError):
    def __init__(self, size: ImageSize):
        self.size = size

    def __str__(self):
        return f"All map images should be square. {self.size.w} x {self.size.h} px."


class ChunkSizesNotSame(RegionScaleError):
    def __init__(self, sizes: set[ImageSize]):
        self.sizes = sizes

    def __str__(self):
        return (
            "All map images should be same resolution. "
            f"Images have {len(self.sizes)} different sizes."
        )
