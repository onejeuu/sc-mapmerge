import os
from pathlib import Path

from scmapmerge.consts import AssetsPath
from scmapmerge.datatype import FoundPath


def subtract_relative_subpath(absolute: Path, relative: Path) -> Path:
    return absolute.parents[len(relative.parts) - 1]


def get_environment_paths() -> list[str]:
    environment_path = os.environ.get("PATH", "")
    return environment_path.split(os.pathsep)


def path_is_matching(path: str) -> bool:
    return path.lower().endswith(str(AssetsPath.ENVIRONMENT))


def find_assets_paths() -> list[FoundPath]:
    environment_paths = get_environment_paths()

    matching_paths: set[FoundPath] = set()

    for path in environment_paths:
        if path_is_matching(path):
            game = subtract_relative_subpath(Path(path), AssetsPath.BIN)
            pda = Path(game, AssetsPath.PDA)

            if pda.exists():
                matching_paths.add(FoundPath(game, pda))

    return list(matching_paths)
