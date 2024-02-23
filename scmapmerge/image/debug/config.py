from scmapmerge.datatype import Color


class Draw:
    TEXT = True
    OUTLINE = True


class Colors:
    CYAN = DEFAULT = Color(0, 255, 255)
    TEXT = DEFAULT
    OUTLINE = DEFAULT


class FontSize:
    FACTOR = 32
    MINIMUM = 16
