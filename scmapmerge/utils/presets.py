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
    crop: Optional[Box] = None
    """Optional relative coordinates of crop in pixels. Right and Bottom is offset."""

    regions: list[Region]
    """List of required regions."""

    @property
    def name(self) -> str:
        return self.__class__.__name__.lower()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}> {self.name} crop={self.crop}"


class Zone(BasePreset):
    crop = Box(0, 0, 1, 264)
    regions = bounds(Box(-12, -3, -6, 9))

class NewSever(BasePreset):
    crop = Box(398, 229, 0, 352)
    regions = bounds(Box(-23, -1, -14, 9))

class UnderArmsklad(BasePreset):
    crop = Box(1947, 1139, 97, 1143)
    regions = bounds(Box(-2, -10, -1, -9))

class UnderPd(BasePreset):
    crop = Box(639, 1222, 50, 744)
    regions = bounds(Box(-3, -10, -2, -9))

class Xvoiniy(BasePreset):
    crop = Box(347, 84, 276, 138)
    regions = bounds(Box(6, -5, 8, -4))

class Kvartali(BasePreset):
    crop = Box(114, 82, 38, 68)
    regions = bounds(Box(9, -5, 10, -4))

class RozaVetrov(BasePreset):
    crop = Box(409, 218, 21, 252)
    regions = bounds(Box(7, 4, 11, 8))

class Nizina(BasePreset):
    crop = Box(250, 0, 250, 420)
    regions = bounds(Box(13, 4, 16, 7))

class Sovhoz(BasePreset):
    crop = Box(387, 42, 315, 383)
    regions = bounds(Box(-4, 4, 0, 8))

class SovhozFull(BasePreset):
    regions = bounds(Box(-4, 1, 3, 8))

class Boral2023(BasePreset):
    regions = bounds(Box(5, -3, 10, 2))

class Boral2021(BasePreset):
    regions = bounds(Box(13, -3, 18, 2))

class GawrGura(BasePreset):
    crop = Box(139, 404, 340, 66)
    regions = [Region(-5, 10)]


# pep8 crime, not best implementation, but still
PRESETS = [
    Zone(),
    NewSever(),
    UnderArmsklad(),
    UnderPd(),
    Xvoiniy(),
    Kvartali(),
    RozaVetrov(),
    Nizina(),
    Sovhoz(),
    SovhozFull(),
    Boral2023(),
    Boral2021(),
    GawrGura()
]
