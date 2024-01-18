from PIL import Image, ImageDraw, ImageFont

from scmapmerge.datatype import Color, ImgCoords, ImgSize, Rectangle
from scmapmerge.utils.region import RegionFile


class Draw:
    TEXT = True
    OUTLINE = True


class Colors:
    CYAN = DEFAULT = Color(0, 255, 255)
    TEXT = DEFAULT
    OUTLINE = DEFAULT


class FontSize:
    FACTOR = 32
    MINIMUM = 16


class DebugRender:
    def __init__(self, img: Image.Image, scale: int):
        self.scale = scale
        self.font = self._load_font()

        self._img = img
        self._imgdraw = ImageDraw.Draw(img)

    def _load_font(self) -> ImageFont.ImageFont:
        size = max(FontSize.MINIMUM, self.scale // FontSize.FACTOR)
        return ImageFont.load_default(size)

    def draw_text(self, text: str) -> None:
        self._imgdraw.text(
            text=text,
            xy=ImgCoords(16, 4),
            font=self.font,
            fill=Colors.TEXT
        )

    def draw_rect(self, rect: Rectangle, outline: Color) -> None:
        self._imgdraw.rectangle(
            xy=rect,
            outline=outline,
            width=4
        )

    def draw(self, region: RegionFile, coords: ImgCoords, scale: int) -> None:
        if Draw.TEXT:
            x, y = coords
            text = "\n".join([
                str(region.path.stem),
                f"{x // scale} {y // scale}",
                f"{x}px {y}px",
            ])
            self.draw_text(text)

        if Draw.OUTLINE:
            outline_rect = Rectangle(
                ImgCoords(1, 1),
                ImgSize(self._img.width - 1, self._img.height - 1)
            )
            self.draw_rect(outline_rect, Colors.OUTLINE)
