from pathlib import Path

from rich import print
from rich.progress import Progress
from rich.prompt import Confirm
from scfile import ol_to_dds
from scfile.exceptions import ScFileException
from PIL import Image

from mapmerge import exceptions as exc
from mapmerge.consts import MIN_FILESIZE, MapSettings, Folder, Prefix
from mapmerge.region import Region, RegionsList
from mapmerge.workspace import Workspace
from mapmerge.utils import ImgSize, Coords


class MapMerger:
    def __init__(self):
        self.workspace = Workspace()
        self.workspace.prepare()

    def run(self):
        self.ask_to_clear()

        if not self.ask_to_skip_converting():
            self.convert_to_dds()

        self.merge_to_full_map()

    def ask_to_clear(self):
        if not self.workspace.is_empty(Folder.CONVERTED):
            print()
            if Confirm.ask(
                (
                    f"{Prefix.QUESTION} \"Converted\" folder is not empty. "
                    "Clean it up?"
                ),
                default=False
            ):
                self.workspace.clear(Folder.CONVERTED)

    def ask_to_skip_converting(self):
        if not self.workspace.is_empty(Folder.CONVERTED):
            print()
            return Confirm.ask(
                f"{Prefix.QUESTION} Skip step converting to .dds?",
                default=True
            )

    def convert_to_dds(self):
        ol_files = self.workspace.ol_files

        if not ol_files:
            raise exc.FolderIsEmpty(folder=Folder.ORIGINAL)

        if self.ask_to_skip_empty_maps() and self._contains_empty_maps(ol_files):
            ol_files = [f for f in ol_files if f.stat().st_size > MIN_FILESIZE]

        print()
        print(Prefix.CONVERTING, "[b]Converting files to dds...[/]")

        with Progress() as self.progress:
            self.task_id = self.progress.add_task(Prefix.PROGRESS, total=len(ol_files))

            for path_ol in ol_files:
                self.convert_ol_file(path_ol)

            self.progress.update(self.task_id, description=f"{Prefix.DONE} [b green]Done[/]")

    def convert_ol_file(self, path_ol: Path):
        path_dds = Path(Folder.CONVERTED, path_ol.with_suffix(".dds").name)

        try:
            ol_to_dds(str(path_ol), str(path_dds))

        except ScFileException:
            raise exc.ScFileError(filename=path_ol.as_posix())

        self.progress.update(self.task_id, advance=1)

    def ask_to_skip_empty_maps(self):
        print()
        return Confirm.ask(
            (
                f"{Prefix.QUESTION} Files contains empty maps. Skip them?\n"
                "(Strictly recommended, otherwise image can turn out incredibly large)"
            ),
            default=True
        )

    def merge_to_full_map(self):
        dds_files = self.workspace.dds_files

        if not dds_files:
            raise exc.FolderIsEmpty(folder=Folder.CONVERTED)

        regions = [Region(path) for path in dds_files]
        regions = RegionsList(*regions)
        regions.sort()

        self._find_chunk_size(regions)

        width = (regions.width + 1) * self.chunk_size
        height = (regions.height + 1) * self.chunk_size

        resolution = width * height

        if resolution >= MapSettings.RESOLUTION_LIMIT:
            raise exc.ImageResolutionLimit(f"Output image is to big - {resolution}px")

        output_image = Image.new(
            mode="RGB",
            size=(width, height),
            color=MapSettings.BACKGROUND_COLOR
        )

        print()
        print(Prefix.MERGE, "[b]Merging to full map...[/]")

        with Progress() as progress:
            task_id = progress.add_task(Prefix.PROGRESS, total=len(regions))

            for region in regions:
                with Image.open(region.path) as img:
                    output_image.paste(img, self._get_image_coordinates(region, regions))

                progress.update(task_id, advance=1)
            progress.update(task_id, description=f"{Prefix.DONE} [b green]Done[/]")

        print()
        print(Prefix.SAVE, "[b]Saving file...[/]")

        output_image.save(f"{Folder.OUTPUT}/{MapSettings.FILENAME}.png")

        print(Prefix.OUTPUT, f"[b purple]Image saved in[/] '{Folder.OUTPUT.as_posix()}' [b purple]folder.[/]")

        print()
        input("Press Enter to exit...")

    def _find_chunk_size(self, regions: RegionsList) -> None:
        sizes: list[ImgSize] = []

        for region in regions:
            with Image.open(region.path) as img:
                sizes.append(ImgSize(w=img.width, h=img.height))

        if not all(w == h for w, h in sizes):
            raise exc.ImageIsNotSquare("Map images should be square.")

        if not all(size == sizes[0] for size in sizes):
            raise exc.ImagesSizesNotSame("Map images should be same size.")

        self.chunk_size = sizes[0]

    def _get_image_coordinates(self, region: Region, regions: RegionsList) -> Coords:
        x = (region.x - regions.min_x) * self.chunk_size
        y = (region.z - regions.min_z) * self.chunk_size

        return Coords(x, y)

    def _contains_empty_maps(self, files: list[Path]):
        for entry in files:
            if entry.is_file() and entry.stat().st_size < MIN_FILESIZE:
                return True
        return False
