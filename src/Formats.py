from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


class Format(NamedTuple):
    OL = ".ol"
    DDS = ".dds"


@dataclass
class OlFormat:
    encoded: str
    decoded: bytes


class OlFormats(Enum):
	DXT1 = OlFormat("3VGGGGGGGGGGGG", b"DXT1")
	DXT5 = OlFormat("3RGGGGGGGGGGGG", b"DXT5")
	RGBA = OlFormat("5&_GGGGGGGGGGG", b"RGBA")
	DXT8BIT = OlFormat("8?>GGGGGGGGGG", b"RGBA")
