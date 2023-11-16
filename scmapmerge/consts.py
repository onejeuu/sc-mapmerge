from pathlib import Path
from typing import NamedTuple


VERSION = "1.2"


# ? 10KB
MIN_FILESIZE = 10240

# ? (r, g, b)
MAP_BACKGROUND_COLOR = (0, 0, 0)


class Defaults(NamedTuple):
    FILENAME = "Map"

    # ? to prevent memory overflow
    RESOLUTION_LIMIT = 1_000_000_000

    # ? png compression level
    COMPRESS_LEVEL = 6


class Folder(NamedTuple):
    WORKSPACE = Path("workspace")
    ENCRYPTED = Path(WORKSPACE, "1-encrypted")
    CONVERTED = Path(WORKSPACE, "2-converted")
    OUTPUT =    Path(WORKSPACE, "3-output")
