from scmapmerge.datatype import Box, Preset, Region


def bounds(box: Box) -> list[Region]:
    return [
        Region(x, z)
        for x in range(box.left, box.right + 1)
        for z in range(box.top, box.bottom + 1)
    ]


PRESETS = [
    Preset(
        "zone",
        regions=bounds(Box(-12, -3, -6, 9)),
        crop=Box(0, 0, 1, 264)
    ),
    Preset(
        "newsever",
        regions=bounds(Box(-23, -1, -14, 9)),
        crop=Box(398, 229, 0, 352)
    ),
    Preset(
        "underarmsklad",
        regions=bounds(Box(-2, -10, -1, -9)),
        crop=Box(1947, 1139, 97, 1143)
    ),
    Preset(
        "underpd",
        regions=bounds(Box(-3, -10, -2, -9)),
        crop=Box(639, 1222, 50, 744)
    ),
    Preset(
        "xvoiniy",
        regions=bounds(Box(6, -5, 8, -4)),
        crop=Box(347, 84, 276, 138)
    ),
    Preset(
        "kvartali",
        regions=bounds(Box(9, -5, 10, -4)),
        crop=Box(114, 82, 38, 68)
    ),
    Preset(
        "rozavetrov",
        regions=bounds(Box(7, 4, 11, 8)),
        crop=Box(409, 218, 21, 252)
    ),
    Preset(
        "nizina",
        regions=bounds(Box(13, 4, 16, 7)),
        crop=Box(250, 0, 250, 420)
    ),
    Preset(
        "sovhoz",
        regions=bounds(Box(-4, 4, 0, 8)),
        crop=Box(387, 42, 315, 383)
    ),
    Preset(
        "sovhozfull",
        regions=bounds(Box(-4, 1, 3, 8))
    ),
    Preset(
        "boral2023",
        regions=bounds(Box(5, -3, 10, 2))
    ),
    Preset(
        "boral2021",
        regions=bounds(Box(13, -3, 18, 2))
    ),
    Preset(
        "gawrgura",
        regions=[Region(-5, 10)],
        crop=Box(139, 404, 340, 66)
    )
]
