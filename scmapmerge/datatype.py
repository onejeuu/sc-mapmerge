from typing import NamedTuple


class Coords(NamedTuple):
    """Coordinates. x and y."""
    x: int
    y: int


class ImgSize(NamedTuple):
    """Image Size in pixels. width and height"""
    w: int
    h: int

    @property
    def resolution(self):
        return self.w * self.h


class Color(NamedTuple):
    """RGB Colors. red, green and blue."""
    r: int
    g: int
    b: int


class Rectangle(NamedTuple):
    """Draw Rectangle. coordinates and size."""
    xy: Coords
    size: ImgSize
