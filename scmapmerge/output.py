from pathlib import Path
from typing import NamedTuple

from PIL import Image, ImageDraw, ImageFont

from scmapmerge.consts import MAP_BACKGROUND_COLOR, Defaults, Folder
from scmapmerge.datatype import Color, Coords, ImgSize, Rectangle
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
                DebugRender(img, scale=regions.scale).draw(region, x, y, xy)

            if self.image_created:
                self._image.paste(img, xy)

    def save(self, path: Path) -> None:
        if self.image_created:
            self._image.save(
                fp=path,
                compress_level=self.compress
            )


class Debug(NamedTuple):
    DRAW_TEXT = True
    DRAW_OUTLINE = True

    DEFAULT_COLOR = Color(0, 255, 255)
    TEXT_COLOR = DEFAULT_COLOR
    OUTLINE_COLOR = DEFAULT_COLOR

    OUTLINE_WIDTH = 4

    FONT_FILE = "RobotoMono.ttf"
    FONT_SIZE_FACTOR = 32
    FONT_SIZE_MINIMUM = 16


class DebugRender:
    def __init__(self, img: Image.Image, scale: int):
        self.scale = scale
        self.font = ImageFont.truetype(self.font_path, self.font_size)

        self._img = img
        self._imgdraw = ImageDraw.Draw(img)

    @property
    def font_path(self) -> str:
        return Path(Folder.ASSETS, Debug.FONT_FILE).as_posix()

    @property
    def font_size(self) -> int:
        return max(Debug.FONT_SIZE_MINIMUM, self.scale // Debug.FONT_SIZE_FACTOR)

    @property
    def outline_rect(self):
        xy = Coords(1, 1)
        size = ImgSize(self._img.width - 1, self._img.height - 1)
        return Rectangle(xy, size)

    def draw_text(self, text: str):
        self._imgdraw.text(Coords(16, 4), text, font=self.font, fill=Debug.TEXT_COLOR)

    def draw_rect(self, rect: Rectangle):
        self._imgdraw.rectangle(rect, outline=Debug.OUTLINE_COLOR, width=Debug.OUTLINE_WIDTH)

    def draw(self, region: Region, x: int, y: int, xy: Coords):
        if Debug.DRAW_TEXT:
            self.draw_text(f"{region.path.stem}\n{x} {y}\n{xy.x}px {xy.y}px")

        if Debug.DRAW_OUTLINE:
            self.draw_rect(self.outline_rect)
