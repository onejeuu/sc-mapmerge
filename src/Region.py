from dataclasses import dataclass

from src.Consts import STRATEGY, CoordsStrategy
from src.Utils import BlockMaxCoords, BlockMinCoords, ImageSize


@dataclass
class Coordinates:
    x: int
    z: int


class Region:
    BLOCK_SIZE = 512
    IMAGE_SIZE = ImageSize()
    MIN = BlockMinCoords()
    MAX = BlockMaxCoords()

    def __init__(self, filename: str) -> None:
        self.filename = filename

        splitted = filename.split('.')

        self.x = int(splitted[1])
        self.z = int(splitted[2])

    @property
    def coordinates(self) -> Coordinates:
        match STRATEGY:
            case CoordsStrategy.CENTER:
                x = int((self.IMAGE_SIZE.width // 2) + (self.x * self.BLOCK_SIZE))
                z = int((self.IMAGE_SIZE.height // 2) + (self.z * self.BLOCK_SIZE))

                return Coordinates(x, z)

            case _:
                min_x = abs(self.MIN.x) if self.MIN.x > 0 else self.MIN.x
                min_z = abs(self.MIN.z) if self.MIN.z > 0 else self.MIN.z
                x = (self.x - min_x) * self.BLOCK_SIZE
                z = (self.z - min_z) * self.BLOCK_SIZE

                return Coordinates(x, z)
