import os
from pathlib import Path

from scmapmerge.consts import AssetsPath
from scmapmerge.datatype import GamePath


def subtract_relative_subpath(absolute: Path, relative: Path) -> Path:
    return absolute.parents[len(relative.parts) - 1]


def get_environment_paths() -> list[str]:
    environment_path = os.environ.get("PATH", "")
    return environment_path.split(os.pathsep)


def path_is_matching(path: str) -> bool:
    return path.lower().endswith(str(AssetsPath.ENVIRONMENT))


def find_assets_paths() -> list[GamePath]:
    environment_paths = get_environment_paths()

    matching_paths: set[GamePath] = set()

    for path in environment_paths:
        if path_is_matching(path):
            runtime = subtract_relative_subpath(Path(path), AssetsPath.BIN)
            game = GamePath(runtime)

            if game.pda.exists():
                matching_paths.add(game)

    return list(matching_paths)
