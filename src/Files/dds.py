from typing import NamedTuple, Any
import numpy as np
import struct

from src.Formats import OlFormats


class DDS(NamedTuple):
    MAGIC = 0x_20534444
    CAPS = 0x_1
    HEIGHT = 0x_2
    WIDTH = 0x_4
    FOURCC = 0x_4
    PIXELFORMAT = 0x_1000
    LINEARSIZE = 0x_80000
    RGB = 0x_40
    ALPHAPIXELS = 0x_1

    R_BITMASK = 0x_00FF0000
    G_BITMASK = 0x_0000FF00
    B_BITMASK = 0x_000000FF
    A_BITMASK = 0x_FF000000

    HEADER_SIZE = 124
    BLOCK_SIZE = 4096
    BIT_COUNT = 32


class DDSHeader:
    SIZE = 128

    def __init__(self):
        self.header = np.zeros(self.SIZE, dtype=np.uint8)

    def add(self, index: int, value: Any, dtype=np.uint8, raw=False):
        self.header[index:index+4] = np.frombuffer(value if raw else struct.pack('<I', value), dtype=dtype)

    def _dxt(self, ol_format_type):
        self.add(80, DDS.FOURCC)
        self.add(84, ol_format_type.value.decoded, raw=True)

    def _rgba(self):
        self.add(80, DDS.RGB | DDS.ALPHAPIXELS)
        self.add(88, DDS.BIT_COUNT)
        self.add(92, DDS.R_BITMASK)
        self.add(96, DDS.G_BITMASK)
        self.add(100, DDS.B_BITMASK)
        self.add(104, DDS.A_BITMASK)

    def _match_format(self, ol_format_type: OlFormats):
        match ol_format_type:
            case OlFormats.DXT1 | OlFormats.DXT5:
                self._dxt(ol_format_type)

            case OlFormats.RGBA:
                self._rgba()

    def create(self, height: int, width: int, decoded_streams: Any, ol_format_type: OlFormats):
        self.add(0, DDS.MAGIC)
        self.add(4, DDS.HEADER_SIZE)
        self.add(8, DDS.CAPS | DDS.PIXELFORMAT | DDS.WIDTH | DDS.HEIGHT | DDS.LINEARSIZE)
        self.add(12, height)
        self.add(16, width)
        self.add(20, len(decoded_streams))
        self.add(76, DDS.BIT_COUNT)

        self._match_format(ol_format_type)

        self.add(108, DDS.BLOCK_SIZE)

    def __iter__(self):
        yield from self.header


class DdsFile:
    def __init__(self, height, width, decoded_streams, ol_format_type):
        self.header = DDSHeader()
        self.header.create(height, width, decoded_streams, ol_format_type)

        self.file_data = bytearray()
        self.file_data.extend(self.header)
        self.file_data.extend(decoded_streams)

    def save(self, output_path):
        with open(output_path, "wb") as f:
            f.truncate(0)
            f.write(self.file_data)
