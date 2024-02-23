from typing import Any, Optional

from click import Context, Parameter, ParamType

from scmapmerge.utils.presets import PRESETS

from .utils import join


class PresetType(ParamType):
    name = "preset"

    def convert(self, value: Any, param: Optional[Parameter], ctx: Optional[Context]):
        for preset in PRESETS:
            if value == preset.name:
                return preset
        self.fail(
            f'Invalid preset "{value}". Available presets: {join(PRESETS)}.', param, ctx
        )
