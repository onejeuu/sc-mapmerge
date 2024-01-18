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


class Rectangle(NamedTuple):
    """Draw Rectangle. coordinates and size."""
    xy: ImgCoords
    size: ImgSize


class Range(NamedTuple):
    """Range. start and stop."""
    start: int
    stop: int
