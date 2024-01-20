from pathlib import Path

from scmapmerge.datatype import ImgSize, Region
from scmapmerge.consts import WEBP_LIMIT


class ScMapMergeException(Exception):
    pass


class RegionError(ScMapMergeException):
    pass


class InvalidRegionFilename(RegionError):
    def __init__(self, path: Path):
        self.path = path

    def __str__(self):
        return f"Region (map image file) '{self.path.as_posix()}' has invalid filename format."


class FolderIsEmpty(ScMapMergeException):
    def __init__(self, folder: Path, hint: str):
        self.folder = folder
        self.hint = hint

    def __str__(self):
        return f"'{self.folder.as_posix()}' folder has no required files. {self.hint}."


class PresetError(ScMapMergeException):
    pass


class MissingRegions(PresetError):
    def __init__(self, preset_name: str, missing: set[Region]):
        self.preset_name = preset_name
        self.missing = missing

    def __str__(self):
        return f"Missing {len(self.missing)} required regions for '{self.preset_name}' preset. "


class ChunkSizeError(ScMapMergeException):
    pass


class ImageIsNotSquare(ChunkSizeError):
    def __init__(self, size: ImgSize):
        self.size = size

    def __str__(self):
        return (
            "All map images should be square. "
            f"{self.size.w} x {self.size.h} px."
        )


class ImagesSizesNotSame(ChunkSizeError):
    def __init__(self, sizes: set[ImgSize]):
        self.sizes = sizes

    def __str__(self):
        return (
            "Map images should be same resolution. "
            f"Images have {len(self.sizes)} different sizes."
        )


class OutputImageError(ScMapMergeException):
    pass


class OutputImageTooLarge(OutputImageError):
    def __init__(self, size: ImgSize, limit: int):
        self.size = size
        self.limit = limit

    def __str__(self):
        return (
            "Output image is too large. "
            f"{self.size.w}px x {self.size.h}px > {self.limit}px."
        )


class WebpResolutionLimit(OutputImageError):
    def __init__(self, size: ImgSize):
        self.size = size

    def __str__(self):
        return (
            f"Webp resolution limit ({WEBP_LIMIT}px) has been reached. "
            f"{self.size.w}px x {self.size.h}px."
        )
