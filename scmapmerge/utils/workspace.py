from pathlib import Path

from scfile.enums import FileSuffix

from scmapmerge.consts import Folder as F
from scmapmerge.exceptions import FolderIsEmpty
from scmapmerge.utils.filename import FileName


class Workspace:
    FOLDERS = [F.WORKSPACE, F.ENCRYPTED, F.CONVERTED, F.OUTPUT]

    def __init__(self, filename: str, suffix: str, overwrite: bool):
        self.filename = filename
        self.suffix = suffix
        self.overwrite = overwrite

    @property
    def exists(self) -> bool:
        """Check that workspace exists."""
        return F.WORKSPACE.exists()

    def is_empty(self, path: Path) -> bool:
        """Check specified path is empty."""
        return not any(path.glob("*"))

    def create_folders(self) -> None:
        """Creates all workspace folders."""
        for folder in self.FOLDERS:
            folder.mkdir(parents=True, exist_ok=True)

    def clear_folder(self, path: Path) -> None:
        """Removes all files from specified path."""
        if path.is_dir() and path.exists():
            for entry in path.glob("*"):
                if entry.is_file():
                    entry.unlink(missing_ok=True)

    def clear_all_folders(self) -> None:
        """Clears all workspace folders."""
        for folder in self.FOLDERS:
            self.clear_folder(folder)

    def get_files(self, path: Path, *suffixes: str) -> list[Path]:
        """List of files in folder with given suffixes."""
        return [
            file for suffix in suffixes
            for file in path.glob(f"*.{suffix}")
        ]

    def get_map_files(self, path: Path, *suffixes: str, hint: str) -> list[Path]:
        """List of files with given suffixes and raises exception if folder is empty."""
        files = self.get_files(path, *suffixes)
        if not files:
            raise FolderIsEmpty(path, hint)
        return files

    def get_encrypted_files(self) -> list[Path]:
        """List of encrypted files in workspace."""
        return self.get_map_files(
            F.ENCRYPTED,
            FileSuffix.OL, FileSuffix.MIC,
            hint="Put encrypted map files there (.ol or .mic)"
        )

    def get_converted_files(self) -> list[Path]:
        """List of converted files in workspace."""
        return self.get_map_files(
            F.CONVERTED,
            FileSuffix.DDS, FileSuffix.PNG,
            hint="Convert map files first"
        )

    def get_output_image_path(self) -> Path:
        """Output image path based on filename template."""
        return FileName(F.OUTPUT, self.filename, self.suffix, self.overwrite).as_path()
