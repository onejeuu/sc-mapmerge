from dataclasses import dataclass

import lz4.block


@dataclass
class ImageSize:
    width = 0
    height = 0


@dataclass
class BlockMinCoords:
    x = 0
    z = 0


@dataclass
class BlockMaxCoords:
    x = 0
    z = 0


class Utils:
    @staticmethod
    def bew_to_lew(value: int) -> int:
        return ((value & 0x_FF00) >> 8) | ((value & 0x_00FF) << 8)

    @staticmethod
    def bedw_to_ledw(value: int) -> int:
        return \
            ((value & 0x_FF000000) >> 24)   | \
            ((value & 0x_00FF0000) >> 8)    | \
            ((value & 0x_0000FF00) << 8)    | \
            ((value & 0x_000000FF) << 24)

    @staticmethod
    def decompress_lz4(f, compressed_size, uncompressed_size) -> bytearray:
        return lz4.block.decompress(f.read(compressed_size), uncompressed_size)
