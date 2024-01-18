from typing import NamedTuple


class Region(NamedTuple):
    """Minecraft region. x and z."""
    x: int
    z: int


class ImgCoords(NamedTuple):
    """Image coordinates. x and y."""
    x: int
    y: int


class Prompt(NamedTuple):
    message: str
    default: bool


class ImgSize(NamedTuple):
    """Image size in pixels. width and height"""
    w: int
    h: int

    @property
    def resolution(self):
        return self.w * self.h


class Color(NamedTuple):
    """RGB colors. red, green and blue."""
    r: int
    g: int
    b: int


class Box(NamedTuple):
    """Box. left, top, right, bottom."""
    left: int
    top: int
    right: int
    bottom: int

    def offset(self, size: ImgSize) -> "Box":
        return Box(self.left, self.top, size.w - self.right, size.h - self.bottom)

    @property
    def valid(self) -> bool:
        return self.right > self.left and self.bottom > self.top


class Rectangle(NamedTuple):
    """Draw Rectangle. coordinates and size."""
    xy: ImgCoords
    size: ImgSize
