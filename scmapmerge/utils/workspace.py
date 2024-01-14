from pathlib import Path

from scmapmerge.consts import Folder as F
from scmapmerge.consts import MapFile
from scmapmerge.exceptions import FolderIsEmpty
from scmapmerge.utils.filename import FileName


class Workspace:
    FOLDERS = [F.WORKSPACE, F.ENCRYPTED, F.CONVERTED, F.OUTPUT]
    SUFFIX = ".png"

    def __init__(self, filename: str):
        self.filename = filename

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
            for file in path.glob("*"):
                if file.is_file():
                    file.unlink(missing_ok=True)

    def clear_all_folders(self) -> None:
        """Clears all workspace folders."""
        for folder in self.FOLDERS:
            self.clear_folder(folder)

    def get_filesize(self, entry: Path) -> int:
        """File size in bytes."""
        return entry.stat().st_size

    def contains_empty_maps(self) -> bool:
        """Checks if encrypted folder contains empty map files."""
        return any(
            self.get_filesize(entry) < MapFile.MINIMUM_SIZE
            for entry in self.get_files(F.ENCRYPTED, ".ol")
        )

    def filter_empty_maps(self, files: list[Path]) -> list[Path]:
        """List of files with filesize > limit."""
        return list(filter(
            lambda entry: self.get_filesize(entry) > MapFile.MINIMUM_SIZE, files
        ))

    def get_files(self, path: Path, *suffixes: str) -> list[Path]:
        """List of files in folder with given suffixes."""
        return [file for suffix in suffixes for file in path.glob(f"*{suffix}")]

    def get_map_files(self, path: Path, *suffixes: str, hint: str) -> list[Path]:
        """List of files with given extensions and raises exception if folder is empty."""
        files = self.get_files(path, *suffixes)
        if not files:
            raise FolderIsEmpty(path, hint)
        return files

    def get_encrypted_files(self) -> list[Path]:
        """List of encrypted files in workspace."""
        return self.get_map_files(F.ENCRYPTED, ".ol", ".mic", hint="Put encrypted map files there (.ol or .mic)")

    def get_converted_files(self) -> list[Path]:
        """List of converted files in workspace."""
        return self.get_map_files(F.CONVERTED, ".dds", ".png", hint="Convert map files first")

    def get_output_image_path(self) -> Path:
        """Output image path based on filename template."""
        filename = FileName(F.OUTPUT, self.filename, self.SUFFIX)
        return filename.as_path()
