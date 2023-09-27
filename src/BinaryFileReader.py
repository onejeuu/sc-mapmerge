import struct


class BinaryFileReader:
    def __init__(self, input_file):
        self.file = input_file

    def _read(self, fmt: str, lenght: int):
        return struct.unpack(f"<{fmt}", self.file.read(lenght))[0]

    def byte(self):
        return self._read("b", 1)

    def bigbyte(self):
        return self._read("B", 1)

    def uword(self):
        return self._read("H", 2)

    def sword(self):
        return self._read("h", 2)

    def udword(self):
        return self._read("I", 4)

    def sdword(self):
        return self._read("i", 4)

    def float(self):
        return self._read("f", 4)

    def zstring(self):
        result = ""
        while True:
            c = self.file.read(1)
            if c == b"\x00":
                break
            result += c.decode("utf-8")
        return result
