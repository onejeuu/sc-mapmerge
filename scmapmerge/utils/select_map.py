from pathlib import Path

from InquirerPy.base.control import Choice

from scmapmerge.datatype import GamePath, MapFolder, Select
from scmapmerge.utils.asker import select
from scmapmerge.utils.find_assets import find_assets_paths
from scmapmerge.workspace.exceptions import AssetsPathNotFound, FolderIsEmpty


MAPS = [
    MapFolder("map", Path("map")),
    MapFolder("under armsklad", Path("map-under_armsklad")),
    MapFolder("under pd", Path("map-under_pd")),
    MapFolder("mogilnik", Path("map-nbolota")),
    MapFolder("bar", Path("map_bar_save")),
    MapFolder("arena raven", Path("map-arena_raven")),
    MapFolder("bolota tutorial", Path("map-dungeon_bolota_tutorial")),
    MapFolder("inside overlay", Path("map_overlay", "inside")),
    MapFolder("sovhoz overlay", Path("map-sovhoz_overlay")),
]


class MapSelector:
    def __init__(self):
        self.game = self.find_game()

    def find_game(self) -> GamePath:
        found_paths = find_assets_paths()

        if not found_paths:
            raise AssetsPathNotFound()

        if len(found_paths) > 1:
            return self.select_assets(found_paths)

        return found_paths[0]

    def select_assets(self, found_paths: list[GamePath]) -> GamePath:
        choices = [Choice(found, name=str(found.assets)) for found in found_paths]

        return select(Select(message="Found multiple game assets. Select one:", choices=choices))

    def select_map(self) -> Path:
        choices: list[Choice] = []

        for map_folder in MAPS:
            map_path = Path(self.game.pda, map_folder.path)

            if map_path.exists():
                choices.append(Choice(map_path, name=map_folder.name))

        if not choices:
            raise FolderIsEmpty(self.game.pda, "Game assets is invalid.")

        return select(Select(message="Select map:", choices=choices))
