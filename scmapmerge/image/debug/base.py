from abc import ABC, abstractmethod

from scmapmerge.datatype import ImageCoords
from scmapmerge.region import BaseRegionFile


class BaseDebugRender(ABC):
    @abstractmethod
    def draw(self, region: BaseRegionFile, coords: ImageCoords) -> None:
        pass
