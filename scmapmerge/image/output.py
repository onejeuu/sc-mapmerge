from pathlib import Path

from PIL import Image

from scmapmerge.consts import Defaults, MapBackground
from scmapmerge.datatype import Box, ImgCoords, ImgSize
from scmapmerge.enums import OutputSuffix
from scmapmerge.exceptions import OutputImageTooLarge
from scmapmerge.image.debug import DebugRender
from scmapmerge.utils.region import ConvertedRegions, RegionFile


class OutputImage:
    # TODO: improve: so cursed

    def __init__(
        self,
        suffix: str = Defaults.SUFFIX,
        compress: int = Defaults.COMPRESS_LEVEL,
        quality: int = Defaults.QUALITY,
        limit: int  = Defaults.RESOLUTION_LIMIT,
        debug: bool = Defaults.DEBUG
    ):
        self.suffix = suffix
        self.compress = compress
        self.quality = quality
        self.limit = limit
        self.debug = debug

    @property
    def image_created(self) -> bool:
        return hasattr(self, "_image") and isinstance(self._image, Image.Image)

    def create_image(self, regions: ConvertedRegions) -> None:
        size = ImgSize(regions.width, regions.height)

        if size.resolution >= self.limit:
            raise OutputImageTooLarge(size, self.limit)

        self._image = Image.new(
            mode="RGB",
            size=size,
            color=MapBackground.COLOR
        )

        if self.suffix != OutputSuffix.JPG:
            self._image.putalpha(MapBackground.ALPHA)

    def paste(self, region: RegionFile, regions: ConvertedRegions) -> None:
        x = region.x - regions.min_x
        y = region.z - regions.min_z

        xy = ImgCoords(x * regions.scale, y * regions.scale)

        with Image.open(region.path) as img:
            if self.debug:
                render = DebugRender(img, scale=regions.scale)
                render.draw(region, x, y, xy)

            if self.image_created:
                self._image.paste(img, xy)

    def crop(self, box: Box):
        if self.image_created:
            size = ImgSize(*self._image.size)

            offset_box = Box(
                left=box.left,
                top=box.top,
                right=size.w + box.right,
                bottom=size.h + box.bottom
            )

            self._image = self._image.crop(offset_box)

    def save(self, path: Path) -> None:
        if self.image_created:
            self._image.save(
                fp=path,
                compress_level=self.compress,
                quality=self.quality
            )
