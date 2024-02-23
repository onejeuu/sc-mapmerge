from PIL import Image, ImageDraw, ImageFont

from scmapmerge.datatype import ImageCoords, ImageSize, Rectangle
from scmapmerge.region import BaseRegionFile

from .base import BaseDebugRender
from .config import Colors, Draw, FontSize


class DebugRender(BaseDebugRender):
    def __init__(self, img: Image.Image, scale: int):
        self.scale = scale
        self.font = self._load_font()

        self._img = img
        self._draw = ImageDraw.Draw(img)

    def _load_font(self) -> ImageFont.ImageFont:
        size = max(FontSize.MINIMUM, self.scale // FontSize.FACTOR)
        return ImageFont.load_default(size)

    def draw(self, region: BaseRegionFile, coords: ImageCoords) -> None:
        if Draw.TEXT:
            x, y = coords
            text = "\n".join(
                [
                    str(region.path.stem),
                    f"{x // self.scale} {y // self.scale}",
                    f"{x}px {y}px",
                ]
            )
            self.text(text)

        if Draw.OUTLINE:
            outline_rect = Rectangle(
                ImageCoords(1, 1), ImageSize(self._img.width - 1, self._img.height - 1)
            )
            self.rect(outline_rect)

    def text(self, text: str) -> None:
        self._draw.text(
            text=text, xy=ImageCoords(16, 4), font=self.font, fill=Colors.TEXT
        )

    def rect(self, rect: Rectangle) -> None:
        self._draw.rectangle(xy=rect, outline=Colors.OUTLINE, width=4)
