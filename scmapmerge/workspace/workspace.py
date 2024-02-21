from pathlib import Path

from scfile.enums import FileSuffix

from scmapmerge.consts import Defaults
from scmapmerge.consts import Folder as F
from scmapmerge.utils.filename import FileName
from scmapmerge.workspace.exceptions import FolderIsEmpty

from .base import BaseWorkspace


class Workspace(BaseWorkspace):
    def __init__(
        self,
        filename: str = Defaults.FILENAME,
        suffix: str = Defaults.SUFFIX,
        overwrite: bool = Defaults.OVERWRITE
    ):
        self.filename = filename
        self.suffix = suffix
        self.overwrite = overwrite

    @property
    def folders(self):
        return [F.WORKSPACE, F.ENCRYPTED, F.CONVERTED, F.OUTPUT]

    @property
    def exists(self):
        return F.WORKSPACE.exists()

    def create(self):
        for folder in self.folders:
            folder.mkdir(parents=True, exist_ok=True)

    def clear(self) -> None:
        for folder in self.folders:
            self.clear_folder(folder)

    def clear_folder(self, path: Path):
        if all((path.exists(), path.is_dir(), path.is_relative_to(F.WORKSPACE))):
            self._clear_folder(path)

    def _clear_folder(self, path: Path):
        for entry in path.glob("*"):
            if entry.is_file():
                entry.unlink(missing_ok=True)

    def get_encrypted_files(self) -> list[Path]:
        return self._get_map_files(
            F.ENCRYPTED, FileSuffix.OL, FileSuffix.MIC,
            hint="Copy encrypted map files there."
        )

    def get_converted_files(self) -> list[Path]:
        return self._get_map_files(
            F.CONVERTED, FileSuffix.DDS, FileSuffix.PNG,
            hint="Convert map files first."
        )

    def get_output_image_path(self) -> Path:
        return FileName(F.OUTPUT, self.filename, self.suffix, self.overwrite).as_path()

    def _get_files(self, path: Path, *suffixes: str) -> list[Path]:
        return [file for suffix in suffixes for file in path.glob(f"*.{suffix}")]

    def _get_map_files(self, path: Path, *suffixes: str, hint: str) -> list[Path]:
        if files := self._get_files(path, *suffixes):
            return files
        raise FolderIsEmpty(path, hint)
