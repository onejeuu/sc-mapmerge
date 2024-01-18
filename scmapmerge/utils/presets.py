from abc import ABC
from typing import Optional

from scmapmerge.datatype import Box, Region


def bounds(box: Box):
    return [
        Region(x, z)
        for x in range(box.left, box.right + 1)
        for z in range(box.top, box.bottom + 1)
    ]


class BasePreset(ABC):
    name: str
    """Lowercase unique name."""

    crop: Optional[Box] = None
    """Optional relative coordinates of crop in pixels. Right and Bottom is offset."""

    regions: list[Region]
    """List of required regions."""

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}> {self.name} crop={self.crop}"


class ZonePreset(BasePreset):
    name = "zone"

    crop = Box(0, 0, 1, 264)
    regions = bounds(Box(-12, -3, -6, 9))


class NewNorthPreset(BasePreset):
    name = "newsever"

    crop = Box(398, 229, 0, 352)
    regions = bounds(Box(-23, -1, -14, 9))


class UnderArmsklad(BasePreset):
    name = "underarmsklad"

    crop = Box(1947, 1139, 97, 1143)
    regions = bounds(Box(-2, -10, -1, -9))


class UnderPd(BasePreset):
    name = "underpd"

    crop = Box(639, 1222, 50, 744)
    regions = bounds(Box(-3, -10, -2, -9))


class GawrGuraPreset(BasePreset):
    name = "gawrgura"

    crop = Box(139, 404, 340, 66)
    regions = [Region(-5, 10)]


PRESETS = [ZonePreset(), NewNorthPreset(), UnderArmsklad(), UnderPd(), GawrGuraPreset()]
