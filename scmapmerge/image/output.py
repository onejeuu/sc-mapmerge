from pathlib import Path

from PIL import Image

from scmapmerge.consts import WEBP_LIMIT, Defaults, MapBackground
from scmapmerge.datatype import Box, ImgCoords, ImgSize
from scmapmerge.enums import OutputSuffix
from scmapmerge.exceptions import OutputImageTooLarge, WebpResolutionLimit
from scmapmerge.image.debug import DebugRender
from scmapmerge.utils.region import ConvertedRegions, RegionFile


class OutputImage:
    # TODO: improve: so cursed

    def __init__(
        self,
        suffix: str = Defaults.SUFFIX,
        limit: int  = Defaults.RESOLUTION_LIMIT,
        compress: int = Defaults.COMPRESS_LEVEL,
        quality: int = Defaults.QUALITY,
        debug: bool = Defaults.DEBUG
    ):
        self.suffix = suffix
        self.limit = limit
        self.compress = compress
        self.quality = quality
        self.debug = debug

    @property
    def image_created(self) -> bool:
        return hasattr(self, "_img") and isinstance(self._img, Image.Image)

    @property
    def size(self) -> ImgSize:
        if not self.image_created:
            return ImgSize(0, 0)
        return ImgSize(*self._img.size)

    def create_image(self, regions: ConvertedRegions) -> None:
        size = ImgSize(regions.width, regions.height)

        if size.resolution >= self.limit:
            raise OutputImageTooLarge(size, self.limit)

        if self.suffix == OutputSuffix.WEBP and any(i >= WEBP_LIMIT for i in size):
            raise WebpResolutionLimit(size)

        self._img = Image.new(
            mode="RGB",
            size=size,
            color=MapBackground.COLOR
        )

        if self.suffix != OutputSuffix.JPG:
            self._img.putalpha(MapBackground.ALPHA)

    def paste(self, region: RegionFile, regions: ConvertedRegions) -> None:
        x = region.x - regions.min_x
        y = region.z - regions.min_z

        xy = ImgCoords(x * regions.scale, y * regions.scale)

        with Image.open(region.path) as img:
            if self.debug:
                render = DebugRender(img, scale=regions.scale)
                render.draw(region, x, y, xy)

            if self.image_created:
                self._img.paste(img, xy)

    def crop(self, box: Box):
        if self.image_created:
            offset_box = Box(
                left=box.left,
                top=box.top,
                right=self.size.w + box.right,
                bottom=self.size.h + box.bottom
            )

            self._img = self._img.crop(offset_box)

    def save(self, path: Path) -> None:
        if self.image_created:
            self._img.save(
                fp=path,
                compress_level=self.compress,
                quality=self.quality
            )
