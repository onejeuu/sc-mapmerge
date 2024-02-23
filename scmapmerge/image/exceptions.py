from scmapmerge.consts import OutputFile
from scmapmerge.datatype import ImageSize
from scmapmerge.exceptions import ScMapMergeException


class ImageError(ScMapMergeException):
    pass


class OutputImageError(ImageError):
    pass


class OutputImageTooLarge(OutputImageError):
    def __init__(self, size: ImageSize, limit: int):
        self.size = size
        self.limit = limit

    def __str__(self):
        return (
            "Output image is too large. "
            f"{self.size.w}px x {self.size.h}px > {self.limit}px."
        )


class WebpResolutionLimit(OutputImageError):
    def __init__(self, size: ImageSize):
        self.size = size

    def __str__(self):
        return (
            f"Webp resolution limit ({OutputFile.WEBP_LIMIT}px) has been reached. "
            f"{self.size.w}px x {self.size.h}px."
        )
