from typing import Optional

from scmapmerge.datatype import Preset, Region

from .listing import RegionsListing


class EncryptedRegions(RegionsListing):
    preset: Optional[Preset] = None

    @property
    def preset_regions(self) -> list[Region]:
        if self.preset:
            return self.preset.regions
        return []

    @property
    def possible_overlay(self) -> bool:
        return self.suffix == ".mic"

    @property
    def contains_empty(self) -> bool:
        return any(
            r.is_empty and r.region not in self.preset_regions for r in self.regions
        )

    @property
    def regions_set(self) -> set[Region]:
        return set(r.region for r in self.regions)

    @property
    def contains_preset(self) -> bool:
        return self.regions_set.issuperset(set(self.preset_regions))

    @property
    def missing_preset(self) -> set[Region]:
        return set(self.preset_regions) - self.regions_set

    def filter_empty(self):
        self.filter(lambda r: not r.is_empty or r.region in self.preset_regions)

    def filter_preset(self):
        self.filter(lambda r: r.region in self.preset_regions)

    def __str__(self):
        return str(self.regions)
