from abc import ABC, abstractmethod
from pathlib import Path

from scmapmerge.datatype import Box, ImageSize
from scmapmerge.region import BaseRegionFile, ConvertedRegions


class BaseOutputImage(ABC):
    regions: ConvertedRegions

    @property
    @abstractmethod
    def size(self) -> ImageSize:
        pass

    @property
    @abstractmethod
    def format(self) -> str:
        pass

    @abstractmethod
    def create(self) -> None:
        """Create new image based on regions size."""
        pass

    @abstractmethod
    def paste(self, region: BaseRegionFile) -> None:
        """Paste region chunk image onto output image."""
        pass

    @abstractmethod
    def crop(self, box: Box) -> None:
        pass

    @abstractmethod
    def save(self, path: Path) -> None:
        pass
