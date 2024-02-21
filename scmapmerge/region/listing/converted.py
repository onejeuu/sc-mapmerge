from PIL import Image

from scmapmerge.datatype import Box, ImageCoords, ImageSize
from scmapmerge.region import BaseRegionFile
from scmapmerge.region.exceptions import ChunkNotSquare, ChunkSizesNotSame

from .listing import RegionsListing


class ConvertedRegions(RegionsListing):
    scale: int = 512

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
    def size(self) -> ImageSize:
        return ImageSize(self.width * self.scale, self.height * self.scale)

    def region_to_xy(self, region: BaseRegionFile) -> ImageCoords:
        x = region.x - self.bounds.left
        y = region.z - self.bounds.top

        return ImageCoords(x * self.scale, y * self.scale)

    def find_scale(self) -> int:
        sizes: set[ImageSize] = set()

        # Check that all images are square
        for region in self.regions:
            with Image.open(region.path) as img:
                size = ImageSize(*img.size)

                if size.w != size.h:
                    raise ChunkNotSquare(size)

                sizes.add(size)

        # Check that all images have the same resolution
        if len(sizes) != 1:
            raise ChunkSizesNotSame(sizes)

        size = sizes.pop()

        self.scale = size.w
        return self.scale
