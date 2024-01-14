from pathlib import Path
from typing import NamedTuple

from scmapmerge.datatype import Color


VERSION = "1.4"


class MapFile(NamedTuple):
    # ? 7KB
    MINIMUM_SIZE = 7168


class MapBackground(NamedTuple):
    COLOR = Color(0, 0, 0)
    ALPHA = 0


class Defaults(NamedTuple):
    FILENAME = "Map %Y.%m.%d.png"

    # ? to prevent memory overflow
    RESOLUTION_LIMIT = 1_000_000_000

    # ? png compression level
    COMPRESS_LEVEL = 6

    DEBUG = False


class Folder(NamedTuple):
    WORKSPACE = Path("workspace")
    ENCRYPTED = Path(WORKSPACE, "1-encrypted")
    CONVERTED = Path(WORKSPACE, "2-converted")
    OUTPUT = Path(WORKSPACE, "3-output")
