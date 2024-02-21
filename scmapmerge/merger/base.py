from abc import ABC, abstractmethod


class BaseMapMerger(ABC):
    @abstractmethod
    def merge(self) -> None:
        """Start entire merging process."""
        pass

    @abstractmethod
    def save_output(self) -> None:
        """Saving output image file."""
        pass
