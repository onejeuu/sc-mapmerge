from pathlib import Path

from PIL import Image, ImageDraw

from scmapmerge.consts import OutputFile, Defaults, MapBackground
from scmapmerge.datatype import Box, Color, ImageCoords, ImageSize
from scmapmerge.enums import OutputFormat
from scmapmerge.image.debug.debug import DebugRender
from scmapmerge.image.exceptions import OutputImageTooLarge, WebpResolutionLimit
from scmapmerge.region import BaseRegionFile

from .base import BaseOutputImage


class OutputImage(BaseOutputImage):
    def __init__(
        self,
        suffix: str = Defaults.SUFFIX,
        limit: int = Defaults.RESOLUTION_LIMIT,
        compress: int = Defaults.COMPRESS_LEVEL,
        quality: int = Defaults.QUALITY,
        debug: bool = Defaults.DEBUG,
    ):
        self.suffix = suffix
        self.limit = limit
        self.compress = compress
        self.quality = quality
        self.debug = debug

        self._create_blank_image()
        self._write_blank_text()

    @property
    def size(self) -> ImageSize:
        return ImageSize(*self._img.size)

    @property
    def format(self):
        return self.suffix

    @property
    def limit_enabled(self):
        return self.limit > 0

    def _create(self, size: ImageSize, color: Color):
        return Image.new(mode="RGB", size=size, color=color)

    def _create_blank_image(self) -> None:
        self._img = self._create(ImageSize(192, 32), Color(0, 0, 0))

    def _write_blank_text(self):
        draw = ImageDraw.Draw(self._img)
        draw.text(ImageCoords(0, 0), text="IF YOU SEE THIS IMAGE")
        draw.text(ImageCoords(0, 16), text="SOMETHING WENT WRONG")

    def create(self) -> None:
        size = self.regions.size

        self._validate_resolution(size)
        self._validate_webp(size)

        self._img = self._create(size, MapBackground.COLOR)
        self._add_alpha()

    def _validate_resolution(self, size: ImageSize):
        if self.limit_enabled and size.resolution >= self.limit:
            raise OutputImageTooLarge(size, self.limit)

    def _validate_webp(self, size: ImageSize):
        if self.format == OutputFormat.WEBP and any(
            i >= OutputFile.WEBP_LIMIT for i in size
        ):
            raise WebpResolutionLimit(size)

    def _add_alpha(self):
        if self.format not in OutputFile.NONTRANSPARENT_FORMATS:
            self._img.putalpha(MapBackground.ALPHA)

    def paste(self, region: BaseRegionFile) -> None:
        xy = self.regions.region_to_xy(region)

        with Image.open(region.path) as img:
            if self.debug:
                render = DebugRender(img, self.regions.scale)
                render.draw(region, xy)

            self._img.paste(img, xy)

    def crop(self, box: Box) -> None:
        box = box.offset(self.size)

        if box.valid:
            self._img = self._img.crop(box)

    def save(self, path: Path) -> None:
        self._img.save(
            fp=path,
            compress_level=self.compress,
            quality=self.quality,
        )
