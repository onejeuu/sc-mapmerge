from pathlib import Path

from scmapmerge.datatype import Color
from scmapmerge.enums import OutputFormat


VERSION = "2.1"

KILOBYTE = KB = 2**10


class MapFile:
    PREFIX = "r"
    DELIMITER = "."
    MINIMUM_SIZE = 7 * KB


class MapBackground:
    COLOR = Color(0, 0, 0)
    ALPHA = 0


class OutputFile:
    WEBP_LIMIT = 16 * KB
    NONTRANSPARENT_FORMATS = {OutputFormat.JPG, OutputFormat.BMP, OutputFormat.DDS}


class WorkspaceFolder:
    WORKSPACE = Path("workspace")
    ENCRYPTED = WORKSPACE / "1-encrypted"
    CONVERTED = WORKSPACE / "2-converted"
    OUTPUT = WORKSPACE / "3-output"


class AssetsPath:
    BIN = Path("win64", "java", "bin")
    ENVIRONMENT = Path("stalcraft", BIN)
    ASSETS = Path("modassets", "assets")
    PDA = Path(ASSETS, "pda")


class Defaults:
    FILENAME = "Map %Y.%m.%d"
    SUFFIX = OutputFormat.JPG
    RESOLUTION_LIMIT = 1_000_000_000
    COMPRESS_LEVEL = 6
    QUALITY = 90
    DEBUG = False
    OVERWRITE = False
