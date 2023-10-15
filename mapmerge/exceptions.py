from pathlib import Path


class MapMergeException(Exception):
    pass


class FolderIsEmpty(MapMergeException):
    def __init__(self, folder: Path, info=""):
        self.folder = folder
        self.info = info


class ScFileError(MapMergeException):
    def __init__(self, filename: str):
        self.filename = filename


class ImageIsNotSquare(MapMergeException):
    pass


class ImagesSizesNotSame(MapMergeException):
    pass


class ImageResolutionLimit(MapMergeException):
    pass
