from pathlib import Path

from PIL import Image, ImageDraw

from scmapmerge import exceptions as exc
from scmapmerge.consts import WEBP_LIMIT, MapBackground
from scmapmerge.datatype import Box, Color, ImgCoords, ImgSize
from scmapmerge.enums import OutputSuffix
from scmapmerge.image.debug import DebugRender
from scmapmerge.region.file import RegionFile
from scmapmerge.region.listing.converted import ConvertedRegions


class OutputImage:
    def __init__(self, suffix: str, limit: int, compress: int, quality: int, debug: bool):
        self.suffix = suffix
        self.limit = limit
        self.compress = compress
        self.quality = quality
        self.debug = debug

        self._create_blank_image()
        self._write_blank_text()

    def _create(self, size: ImgSize, color: Color):
        return Image.new(mode="RGB", size=size, color=color)

    def _create_blank_image(self) -> None:
        self._img = self._create(
            ImgSize(192, 32),
            Color(0, 0, 0)
        )

    def _write_blank_text(self):
        imgdraw = ImageDraw.Draw(self._img)
        imgdraw.text(ImgCoords(0, 0), text="IF YOU SEE THIS IMAGE")
        imgdraw.text(ImgCoords(0, 16), text="SOMETHING WENT WRONG")

    @property
    def size(self) -> ImgSize:
        return ImgSize(*self._img.size)

    def create_image(self, regions: ConvertedRegions) -> None:
        size = regions.size

        if size.resolution >= self.limit:
            raise exc.OutputImageTooLarge(size, self.limit)

        if self.suffix == OutputSuffix.WEBP and any(i >= WEBP_LIMIT for i in size):
            raise exc.WebpResolutionLimit(size)

        self._img = self._create(size, MapBackground.COLOR)

        if self.suffix != OutputSuffix.JPG:
            self._img.putalpha(MapBackground.ALPHA)

    def paste(self, region: RegionFile, xy: ImgCoords, scale: int) -> None:
        with Image.open(region.path) as img:
            if self.debug:
                render = DebugRender(img, scale)
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
            quality=self.quality
        )
