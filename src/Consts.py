from enum import IntEnum, auto
from typing import NamedTuple
from pathlib import Path


VERSION = "1.0"

BACKGROUND_COLOR = (0, 0, 0)
FILENAME = "Map"

PIXELS_LIMIT = 1_000_000_000


class FOLDER(NamedTuple):
    WORKSPACE = "workspace"
    ORIGINAL = Path(WORKSPACE, "Original")
    CONVERTED = Path(WORKSPACE, "Converted")
    OUTPUT = Path(WORKSPACE, "Output")


class CoordsStrategy(IntEnum):
    DEFAULT = auto()
    CENTER = auto()


STRATEGY = CoordsStrategy.CENTER
