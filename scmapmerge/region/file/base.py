from abc import ABC, abstractmethod
from pathlib import Path

from scmapmerge.datatype import Region


class BaseRegionFile(ABC):
    path: Path
    region: Region

    @property
    @abstractmethod
    def x(self) -> int:
        pass

    @property
    @abstractmethod
    def z(self) -> int:
        pass

    @property
    @abstractmethod
    def filesize(self) -> int:
        pass

    @property
    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def get_new_filename(self, suffix: str) -> str:
        pass
