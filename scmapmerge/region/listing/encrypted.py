from typing import Optional

from scmapmerge.consts import MapFile
from scmapmerge.datatype import Region
from scmapmerge.utils.presets import BasePreset

from .base import RegionsList


class EncryptedRegions(RegionsList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.preset: Optional[BasePreset] = None

    @property
    def preset_regions(self) -> list[Region]:
        if self.preset:
            return self.preset.regions
        return []

    @property
    def contains_empty(self) -> bool:
        return any(
            r.filesize <= MapFile.MINIMUM_SIZE and r.region not in self.preset_regions
            for r in self.regions
        )

    @property
    def regions_set(self) -> set[Region]:
        return set(r.region for r in self.regions)

    @property
    def contains_preset(self) -> bool:
        return self.regions_set.issuperset(set(self.preset_regions))

    @property
    def missing_preset(self) -> set:
        return set(self.preset_regions) - self.regions_set

    def filter_empty(self):
        self.filter(
            lambda r: r.filesize > MapFile.MINIMUM_SIZE or r.region in self.preset_regions
        )

    def filter_preset(self):
        self.filter(
            lambda r: r.region in self.preset_regions
        )

    def __str__(self):
        return str(self.regions)
