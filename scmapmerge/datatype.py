from pathlib import Path
from typing import NamedTuple, Optional

from InquirerPy.base.control import Choice


class Region(NamedTuple):
    """Region horizontal plane. x and z."""

    x: int
    z: int


class ImageCoords(NamedTuple):
    """Image coordinates. x and y."""

    x: int
    y: int


class ImageSize(NamedTuple):
    """Image size in pixels. width and height."""

    w: int
    h: int

    @property
    def resolution(self):
        return self.w * self.h


class Color(NamedTuple):
    """RGB color. red, green and blue."""

    r: int
    g: int
    b: int


class Box(NamedTuple):
    """Box. left, top, right and bottom."""

    left: int
    top: int
    right: int
    bottom: int

    def offset(self, size: ImageSize) -> "Box":
        return Box(self.left, self.top, size.w - self.right, size.h - self.bottom)

    @property
    def valid(self) -> bool:
        return self.right > self.left and self.bottom > self.top


class Rectangle(NamedTuple):
    """Draw Rectangle. coordinates and size."""

    xy: ImageCoords
    size: ImageSize


class Preset(NamedTuple):
    """Preset configuration. name, required regions, and optional image cropping."""

    name: str
    regions: list[Region]
    crop: Optional[Box] = None

    def __str__(self):
        return self.name


class Confirm(NamedTuple):
    """Confirm ask prompt. message and default answer."""

    message: str
    default: bool


class Select(NamedTuple):
    """Select prompt. message and list of choices."""

    message: str
    choices: list[Choice]


class GamePath(NamedTuple):
    """Game assets path. assets path and pda path."""

    assets: Path

    @property
    def pda(self):
        return Path(self.assets, "pda")


class MapFolder(NamedTuple):
    """Pda map folder. select name and path."""

    name: str
    path: Path