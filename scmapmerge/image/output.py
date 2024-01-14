from pathlib import Path

from PIL import Image

from scmapmerge.consts import Defaults, MapBackground
from scmapmerge.datatype import Coords, ImgSize
from scmapmerge.exceptions import OutputImageTooLarge
from scmapmerge.image.debug import DebugRender
from scmapmerge.utils.region import Region, RegionsList


class OutputImage:
    def __init__(
        self,
        limit: int  = Defaults.RESOLUTION_LIMIT,
        compress: int = Defaults.COMPRESS_LEVEL,
        debug: bool = Defaults.DEBUG
    ):
        self.limit = limit
        self.compress = compress
        self.debug = debug

    @property
    def image_created(self) -> bool:
        return hasattr(self, "_image") and isinstance(self._image, Image.Image)

    def create_image(self, regions: RegionsList) -> None:
        size = ImgSize(
            w = regions.width,
            h = regions.height
        )

        if size.resolution >= self.limit:
            raise OutputImageTooLarge(size, self.limit)

        self._image = Image.new(
            mode="RGB",
            size=size,
            color=MapBackground.COLOR
        )

        self._image.putalpha(MapBackground.ALPHA)

    def paste(self, region: Region, regions: RegionsList) -> None:
        x = region.x - regions.min_x
        y = region.z - regions.min_z

        xy = Coords(
            x = x * regions.scale,
            y = y * regions.scale
        )

        with Image.open(region.path) as img:
            if self.debug:
                render = DebugRender(img, scale=regions.scale)
                render.draw(region, x, y, xy)

            if self.image_created:
                self._image.paste(img, xy)

    def save(self, path: Path) -> None:
        if self.image_created:
            self._image.save(
                fp=path,
                compress_level=self.compress
            )
