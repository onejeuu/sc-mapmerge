from pathlib import Path

from scmapmerge.datatype import Color
from scmapmerge.enums import OutputSuffix


VERSION = "1.5-dev"

# ? kibibyte / kilobyte
KB = 2**10

# ? webp resolution limit
WEBP_LIMIT = 16 * KB


class MapFile:
    # ? filename prefix
    PREFIX = "r."

    MINIMUM_SIZE = 7 * KB


class MapBackground:
    COLOR = Color(0, 0, 0)
    ALPHA = 0


class Defaults:
    FILENAME = "Map %Y.%m.%d"
    SUFFIX = OutputSuffix.JPG

    # ? to prevent memory overflow
    RESOLUTION_LIMIT = 1_000_000_000

    # ? compression level (png)
    COMPRESS_LEVEL = 6

    # ? quality (jpg, webp)
    QUALITY = 90

    DEBUG = False


class Folder:
    WORKSPACE = Path("workspace")
    ENCRYPTED = Path(WORKSPACE, "1-encrypted")
    CONVERTED = Path(WORKSPACE, "2-converted")
    OUTPUT = Path(WORKSPACE, "3-output")
