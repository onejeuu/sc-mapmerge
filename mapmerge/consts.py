from pathlib import Path
from typing import NamedTuple


VERSION = "1.0"


# ? 10KB
MIN_FILESIZE = 10240


class MapSettings(NamedTuple):
    FILENAME = "Map"

    # ? (r, g, b)
    BACKGROUND_COLOR = (0, 0, 0)

    # ? to prevent memory overflow
    RESOLUTION_LIMIT = 1_000_000_000


class Folder(NamedTuple):
    WORKSPACE = Path("workspace")
    ORIGINAL = Path(WORKSPACE, "Original")
    CONVERTED = Path(WORKSPACE, "Converted")
    OUTPUT = Path(WORKSPACE, "Output")


class Prefix(NamedTuple):
    QUESTION = "[b yellow]?[/]"
    CONVERTING = "🔄"
    DONE = "✅"
    PROGRESS = "⏳"
    MERGE = "🔗"
    SAVE = "📥"
    OUTPUT = "🦄"
