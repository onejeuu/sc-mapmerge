from pathlib import Path

from PIL import Image

from scmapmerge.consts import MAP_BACKGROUND_COLOR, Defaults
from scmapmerge.exceptions import OutputImageTooLarge
from scmapmerge.region import Region, RegionsList
from scmapmerge.utils import Coords, ImgSize


class OutputImage:
    def __init__(
        self,
        limit: int  = Defaults.RESOLUTION_LIMIT,
        compress: int = Defaults.COMPRESS_LEVEL
    ):
        self.limit = limit
        self.compress = compress

        self._size = ImgSize(0, 0)

    @property
    def resolution(self) -> int:
        return self._size.w * self._size.h

    def create(self, regions: RegionsList):
        self._size = ImgSize(
            w = regions.width,
            h = regions.height
        )

        if self.resolution >= self.limit:
            raise OutputImageTooLarge(self._size, self.limit)

        self._image = Image.new(
            mode="RGB",
            size=self._size,
            color=MAP_BACKGROUND_COLOR
        )

    def paste(self, img: Image.Image, region: Region, regions: RegionsList):
        self._image.paste(
            img,
            Coords(
                x = (region.x - regions.min_x) * regions.scale,
                y = (region.z - regions.min_z) * regions.scale
            )
        )

    def save(self, path: Path):
        self._image.save(
            fp=path,
            compress_level=self.compress
        )
