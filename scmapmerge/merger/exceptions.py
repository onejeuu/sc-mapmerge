from scmapmerge.datatype import Region
from scmapmerge.exceptions import ScMapMergeException


class MergerError(ScMapMergeException):
    pass


class PresetError(MergerError):
    pass


class MissingRegions(PresetError):
    def __init__(self, preset_name: str, missing: set[Region]):
        self.preset_name = preset_name
        self.missing = missing

    def __str__(self):
        return f"Missing {len(self.missing)} required regions for '{self.preset_name}' preset."
