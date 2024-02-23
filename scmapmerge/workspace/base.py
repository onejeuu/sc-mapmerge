from abc import ABC, abstractmethod
from pathlib import Path


class BaseWorkspace(ABC):
    @property
    @abstractmethod
    def folders(self) -> list[Path]:
        pass

    @property
    @abstractmethod
    def exists(self) -> bool:
        pass

    @abstractmethod
    def create(self) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def clear_folder(self, path: Path) -> None:
        pass

    @abstractmethod
    def copy_files_to_encrypted(self, folder: Path) -> None:
        pass

    @abstractmethod
    def get_encrypted_files(self) -> list[Path]:
        pass

    @abstractmethod
    def get_converted_files(self) -> list[Path]:
        pass

    @abstractmethod
    def get_output_image_path(self) -> Path:
        pass
