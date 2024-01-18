from abc import ABC
from typing import Optional

from scmapmerge.datatype import Box, Region, Range


# TODO: improve: quite confusing
def regions_bounds(x: Range, z: Range):
    return [
        Region(region_x, region_z)
        for region_x in range(x.start, x.stop + 1)
        for region_z in range(z.start, z.stop + 1)
    ]


class BasePreset(ABC):
    name: str
    """Lowercase unique name."""

    crop: Optional[Box] = None
    """Optional relative coordinates of crop in pixels."""

    regions: list[Region]
    """List of regions required."""

    def __str__(self):
        return f"<{self.__class__.__name__}> {self.name} crop={self.crop}"


class ZonePreset(BasePreset):
    name = "zone"

    crop = Box(0, 0, -1, -264)

    regions = regions_bounds(
        x = Range(-12, -6),
        z = Range(-3, 9)
    )


class NewNorthPreset(BasePreset):
    name = "newsever"

    crop = Box(398, 229, 0, -352)

    regions = regions_bounds(
        x = Range(-23, -14),
        z = Range(-1, 9)
    )


class GawrGuraPreset(BasePreset):
    name = "gawrgura"

    crop = Box(139, 404, -340, -66)

    regions = [Region(-5, 10)]


PRESETS = [ZonePreset, NewNorthPreset, GawrGuraPreset]
