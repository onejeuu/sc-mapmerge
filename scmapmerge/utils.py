from typing import NamedTuple


class Coords(NamedTuple):
    """Coordinates"""
    x: int
    y: int


class ImgSize(NamedTuple):
    """Image Size in pixels. width and height"""
    w: int
    h: int
