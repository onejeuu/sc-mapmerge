from pathlib import Path
from typing import NamedTuple

from scmapmerge.datatype import Color


VERSION = "1.3"


# ? 7KB
MINIMUM_MAP_FILE_SIZE = 7168

MAP_BACKGROUND_COLOR = Color(0, 0, 0)


class Defaults(NamedTuple):
    FILENAME = "Map"

    # ? to prevent memory overflow
    RESOLUTION_LIMIT = 1_000_000_000

    # ? png compression level
    COMPRESS_LEVEL = 6

    DEBUG = False


class Folder(NamedTuple):
    ASSETS =    Path("assets")
    WORKSPACE = Path("workspace")
    ENCRYPTED = Path(WORKSPACE, "1-encrypted")
    CONVERTED = Path(WORKSPACE, "2-converted")
    OUTPUT =    Path(WORKSPACE, "3-output")
