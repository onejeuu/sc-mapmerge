from typing import NamedTuple

from PIL import Image, ImageDraw, ImageFont

from scmapmerge.datatype import Color, Coords, ImgSize, Rectangle
from scmapmerge.utils.region import Region


class Draw(NamedTuple):
    TEXT = True
    OUTLINE = True


class Colors(NamedTuple):
    DEFAULT = Color(0, 255, 255)
    TEXT = DEFAULT
    OUTLINE = DEFAULT


class FontSize(NamedTuple):
    FACTOR = 32
    MINIMUM = 16


class DebugRender:
    def __init__(self, img: Image.Image, scale: int):
        self.scale = scale
        self.font = self.load_font()

        self._img = img
        self._imgdraw = ImageDraw.Draw(img)

    def load_font(self):
        size = max(FontSize.MINIMUM, self.scale // FontSize.FACTOR)
        return ImageFont.load_default(size)

    @property
    def outline_rect(self):
        xy = Coords(1, 1)
        size = ImgSize(self._img.width - 1, self._img.height - 1)
        return Rectangle(xy, size)

    def draw_text(self, text: str):
        self._imgdraw.text(Coords(16, 4), text, font=self.font, fill=Colors.TEXT)

    def draw_rect(self, rect: Rectangle):
        self._imgdraw.rectangle(rect, outline=Colors.OUTLINE, width=4)

    def draw(self, region: Region, x: int, y: int, coords: Coords):
        if Draw.TEXT:
            self.draw_text(f"{region.path.stem}\n{x} {y}\n{coords.x}px {coords.y}px")

        if Draw.OUTLINE:
            self.draw_rect(self.outline_rect)
