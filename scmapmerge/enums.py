from enum import StrEnum, auto


class OutputFormat(StrEnum):
    """Output image suffix."""

    JPG = auto()
    PNG = auto()
    WEBP = auto()
    TIFF = auto()
    BMP = auto()
    DDS = auto()
