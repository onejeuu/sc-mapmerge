from pathlib import Path
import shutil

from scfile.enums import FileSuffix

from scmapmerge.consts import Defaults
from scmapmerge.consts import WorkspaceFolder as F
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

    def copy_files_to_encrypted(self, folder: Path) -> None:
        files = self._get_files(folder, FileSuffix.OL, FileSuffix.MIC)

        if not files:
            raise FolderIsEmpty(folder, "Game assets is invalid.")

        self.create()

        for file in files:
            shutil.copy(file, F.ENCRYPTED / file.name)

    def get_encrypted_files(self) -> list[Path]:
        folder = F.ENCRYPTED
        files = self._get_files(folder, FileSuffix.OL, FileSuffix.MIC)

        if not files:
            raise FolderIsEmpty(folder, "Copy encrypted map files there.")

        return files

    def get_converted_files(self) -> list[Path]:
        folder = F.CONVERTED
        files = self._get_files(folder, FileSuffix.DDS, FileSuffix.PNG)

        if not files:
            raise FolderIsEmpty(folder, "Convert map files first.")

        return files

    def get_output_image_path(self) -> Path:
        return FileName(F.OUTPUT, self.filename, self.suffix, self.overwrite).as_path()

    def _get_files(self, folder: Path, *suffixes: str) -> list[Path]:
        return [file for suffix in suffixes for file in folder.glob(f"*.{suffix}")]
