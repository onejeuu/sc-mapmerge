from pathlib import Path
import shutil

from scfile.enums import FileSuffix

from scmapmerge.consts import Defaults
from scmapmerge.consts import WorkspaceDirectory as F
from scmapmerge.utils.filename import FileName
from scmapmerge.workspace.exceptions import DirIsEmpty


class Workspace:
    root = F.WORKSPACE

    def __init__(
        self,
        filename: str = Defaults.FILENAME,
        suffix: str = Defaults.SUFFIX,
        overwrite: bool = Defaults.OVERWRITE,
    ):
        self.filename = filename
        self.suffix = suffix
        self.overwrite = overwrite

    @property
    def dirs(self) -> list[Path]:
        return [self.root, F.ENCRYPTED, F.CONVERTED, F.OUTPUT]

    @property
    def exists(self):
        return self.root.exists()

    def create(self):
        for path in self.dirs:
            path.mkdir(parents=True, exist_ok=True)

    def clear(self) -> None:
        for path in self.dirs:
            self.clear_directory(path)

    def clear_directory(self, path: Path):
        if all((path.exists(), path.is_dir(), path.is_relative_to(self.root))):
            self._unlink_files(path)

    def _unlink_files(self, path: Path):
        for entry in path.glob("*"):
            if entry.is_file():
                entry.unlink(missing_ok=True)

    def copy_files_to_encrypted(self, path: Path) -> None:
        files = self._get_files(path, FileSuffix.OL, FileSuffix.MIC)

        if not files:
            raise DirIsEmpty(path, "Game assets is invalid.")

        self.create()

        for file in files:
            shutil.copy(file, F.ENCRYPTED / file.name)

    def get_encrypted_files(self) -> list[Path]:
        path = F.ENCRYPTED
        files = self._get_files(path, FileSuffix.OL, FileSuffix.MIC)

        if not files:
            raise DirIsEmpty(path, "Copy encrypted map files there.")

        return files

    def get_converted_files(self) -> list[Path]:
        path = F.CONVERTED
        files = self._get_files(path, FileSuffix.DDS, FileSuffix.PNG)

        if not files:
            raise DirIsEmpty(path, "Convert map files first.")

        return files

    def get_output_image_path(self) -> Path:
        return FileName(F.OUTPUT, self.filename, self.suffix, self.overwrite).as_path()

    def _get_files(self, path: Path, *suffixes: str) -> list[Path]:
        return [file for suffix in suffixes for file in path.glob(f"*.{suffix}")]
