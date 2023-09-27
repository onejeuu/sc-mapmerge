from src.BinaryFileReader import BinaryFileReader
from src.Files import DdsFile
from src.Formats import OlFormats
from src.Utils import Utils


class OlFile:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

    def _identify_format(self):
        for fmt in OlFormats:
            if fmt.value.encoded in self.ol_format:
                return fmt

        return None

    def _unpack_square(self, color0, color1, indices):
        # kill me

        palette = [0] * 8
        palette[:2] = color0, color1

        if color0 > color1:
            palette[2:] = [((8 - i) * color0 + (i - 1) * color1) // 7 for i in range(2, 8)]
        else:
            palette[2:6] = [((6 - i) * color0 + (i - 1) * color1) // 5 for i in range(2, 6)]
            palette[6:] = [0, 0xFF]

        indices = sum((indices[i] << (i * 8)) for i in range(6))

        unpacked_square = [[0] * 4 for _ in range(4)]

        for i in range(4):
            for j in range(4):
                indices, temp = divmod(indices, 8)
                unpacked_square[i][j] = palette[temp]

        return unpacked_square

    def _unpack_8bit(self):
        if self.width * self.height != len(self.decoded_streams):
            raise Exception("Can't unpack 8-Bit XY DXT - invalid buffer length")

        if self.width % 4 != 0 or self.height % 4 != 0:
            raise Exception("Can't unpack 8-Bit XY DXT - dimensions not multiple of 4")

        unpacked = bytearray(self.width * self.height * 4)

        self._position = 0

        def unpack_square():
            color0, color1, *indices = self.decoded_streams[self._position:self._position + 8]
            self._position += 8
            return self._unpack_square(color0, color1, indices), current_position

        for y in range(self.height // 4):
            for x in range(self.width // 4):
                square_g, current_position = unpack_square()
                square_r, current_position = unpack_square()

                for ky in range(4):
                    for kx in range(4):
                        pixel_index = ((y * 4 + ky) * self.width + (x * 4 + kx)) * 4
                        unpacked[pixel_index:pixel_index + 4] = (0xFF, square_r[ky][kx], square_g[ky][kx], 0xFF)

        return unpacked

    def convert(self):
        with open(self.input_path, "rb") as f:
            read = BinaryFileReader(f)

            # ol magic
            hex(read.udword())

            self.width = Utils.bedw_to_ledw(read.udword())
            self.height = Utils.bedw_to_ledw(read.udword())
            self.streams_count = Utils.bedw_to_ledw(read.udword())

            self.ol_format = read.zstring()

            self.ol_format_type = self._identify_format()

            if not self.ol_format_type:
                return

            uncompressed_sizes = [Utils.bedw_to_ledw(read.udword()) for _ in range(self.streams_count)]
            compressed_sizes = [Utils.bedw_to_ledw(read.udword()) for _ in range(self.streams_count)]

            id_size = Utils.bew_to_lew(read.uword())
            id_str = "".join(chr(read.byte()) for _ in range(id_size))

            self.decoded_streams = Utils.decompress_lz4(f, compressed_sizes[0], uncompressed_sizes[0])

            if self.ol_format_type == OlFormats.DXT8BIT and self.streams_count > 0:
                self.decoded_streams = self._unpack_8bit()
                self.ol_format_type = OlFormats.RGBA

        dds_file = DdsFile(self.height, self.width, self.decoded_streams, self.ol_format_type)
        dds_file.save(self.output_path)

        return (self.width, self.height)
