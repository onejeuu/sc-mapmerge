from pathlib import Path

from scmapmerge.datatype import Color
from scmapmerge.enums import OutputFormat


VERSION = "2.0"

# ? kibibyte / kilobyte
KB = 2**10

# ? webp resolution limit
WEBP_LIMIT = 16 * KB

# ? formats that dont support transparency
NONTRANSPARENT_FORMATS = {OutputFormat.JPG, OutputFormat.BMP, OutputFormat.DDS}

class MapFile:
    PREFIX = "r"
    DELIMITER = "."
    MINIMUM_SIZE = 7 * KB

class MapBackground:
    COLOR = Color(0, 0, 0)
    ALPHA = 0

class Defaults:
    FILENAME = "Map %Y.%m.%d"
    SUFFIX = OutputFormat.JPG
    RESOLUTION_LIMIT = 1_000_000_000 # prevent memory overflow
    COMPRESS_LEVEL = 6 # image compression (png)
    QUALITY = 90 # image quality (jpg, webp)
    DEBUG = False
    OVERWRITE = False

class Folder:
    WORKSPACE = Path("workspace")
    ENCRYPTED = WORKSPACE / "1-encrypted"
    CONVERTED = WORKSPACE / "2-converted"
    OUTPUT = WORKSPACE / "3-output"
