from PIL import Image

from scmapmerge import exceptions as exc
from scmapmerge.datatype import Box, ImgCoords, ImgSize
from scmapmerge.region.file import RegionFile

from .base import RegionsList


class ConvertedRegions(RegionsList):
    DEFAULT_SCALE = 512

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale: int = self.DEFAULT_SCALE

    @property
    def bounds(self) -> Box:
        if not self.regions:
            return Box(0, 0, 0, 0)

        return Box(min(self.x), min(self.z), max(self.x), max(self.z))

    @property
    def width(self):
        return abs(self.bounds.left - self.bounds.right) + 1

    @property
    def height(self):
        return abs(self.bounds.top - self.bounds.bottom) + 1

    @property
    def size(self) -> ImgSize:
        return ImgSize(self.width * self.scale, self.height * self.scale)

    def region_to_xy(self, region: RegionFile) -> ImgCoords:
        """Convert region coordinates to image coordinates."""

        x = region.x - self.bounds.left
        y = region.z - self.bounds.top

        return ImgCoords(x * self.scale, y * self.scale)

    def find_scale(self) -> int:
        """Find chunk size scale for images based on their sizes."""

        sizes: set[ImgSize] = set()

        # Check that all images are square
        for region in self.regions:
            with Image.open(region.path) as img:
                size = ImgSize(*img.size)

                if size.w != size.h:
                    raise exc.ImageIsNotSquare(size)

                sizes.add(size)

        # Check that all images have the same resolution
        if len(sizes) != 1:
            raise exc.ImagesSizesNotSame(sizes)

        size = sizes.pop()

        self.scale = size.w
        return self.scale
