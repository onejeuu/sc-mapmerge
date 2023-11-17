from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from scmapmerge.consts import MAP_BACKGROUND_COLOR, Debug, Defaults
from scmapmerge.datatype import Coords, ImgSize, Rectangle
from scmapmerge.exceptions import OutputImageTooLarge
from scmapmerge.region import Region, RegionsList


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

        self._size = ImgSize(0, 0)

    @property
    def image_created(self) -> bool:
        return isinstance(self._image, Image.Image)

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
            color=MAP_BACKGROUND_COLOR
        )

    def paste(self, region: Region, regions: RegionsList) -> None:
        x = region.x - regions.min_x
        y = region.z - regions.min_z

        xy = Coords(
            x = x * regions.scale,
            y = y * regions.scale
        )

        with Image.open(region.path) as img:
            if self.debug:
                self._draw_debug(
                    img,
                    font_size = self._get_font_size(regions),
                    text = self._get_debug_text(region, x, y, xy)
                )

            if self.image_created:
                self._image.paste(img, xy)

    def save(self, path: Path) -> None:
        if self.image_created:
            self._image.save(
                fp=path,
                compress_level=self.compress
            )

    def _get_font_size(self, regions: RegionsList) -> int:
        return max(Debug.FONT_SIZE_MINIMUM, regions.scale // Debug.FONT_SIZE_FACTOR)

    def _get_debug_text(self, region: Region, x: int, y: int, xy: Coords) -> str:
        return f"{region.path.stem}\n{x} {y}\n{xy.x}px {xy.y}px"

    def _draw_debug(self, img: Image.Image, font_size: int, text: str) -> None:
        draw = ImageDraw.Draw(img)

        if Debug.DRAW_TEXT:
            font = ImageFont.truetype("assets/RobotoMono.ttf", font_size)
            draw.text(Coords(16, 4), text, font=font, fill=Debug.TEXT_COLOR)

        if Debug.DRAW_OUTLINE:
            rect = Rectangle(Coords(1, 1), ImgSize(img.width-1, img.height-1))
            draw.rectangle(rect, outline=Debug.OUTLINE_COLOR, width=Debug.OUTLINE_WIDTH)
