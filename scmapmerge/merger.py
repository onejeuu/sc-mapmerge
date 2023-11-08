from pathlib import Path

import scfile
from PIL import Image
from rich import print

from scmapmerge import exceptions as exc
from scmapmerge.asker import WorkspaceAsker
from scmapmerge.consts import MAP_BACKGROUND_COLOR, Defaults, Folder
from scmapmerge.progress import FilesProgress
from scmapmerge.region import Region, RegionsList
from scmapmerge.utils import Coords, ImgSize
from scmapmerge.workspace import Workspace


class MapMerger:
    def __init__(
        self,
        filename: str = Defaults.FILENAME,
        resolution_limit: int  = Defaults.RESOLUTION_LIMIT,
        compress: int = Defaults.COMPRESS_LEVEL
    ):
        self.filename = filename
        self.resolution_limit = resolution_limit
        self.compress = compress

        self.workspace = Workspace(filename)
        self.asker = WorkspaceAsker(self.workspace)

    def run(self):
        self.check_first_launch()
        self.workspace.create_all()

        self.asker.clear_converted()

        if not self.asker.skip_converting():
            self.convert_to_dds()

        self.merge_to_full_map()

    def check_first_launch(self):
        if not self.workspace.exists:
            self.workspace.create_all()
            print(
                "\n[b yellow]Workspace has been successfully created.\n"
                f"Place .ol files in[/] '{Folder.ENCRYPTED.as_posix()}' [b yellow]folder.[/]"
            )
            input("Press Enter to continue...")

    def convert_to_dds(self):
        ol_files = self.workspace.ol_files

        if not ol_files:
            raise exc.FolderIsEmpty(
                folder=Folder.ENCRYPTED,
                hint="Put .ol files there"
            )

        if self.workspace.contains_empty_maps() and self.asker.skip_empty_maps():
            ol_files = self.workspace.not_empty_ol_files

        self.convert_ol_files(ol_files)

    def convert_ol_files(self, ol_files: list[Path]):
        print()
        print("🔄", "[b]Converting files to dds...[/]")

        with FilesProgress(total=len(ol_files)) as progress:
            for ol in ol_files:
                dds = Path(Folder.CONVERTED, ol.with_suffix(".dds").name)
                scfile.ol_to_dds(str(ol), str(dds))
                progress.increment()

    def merge_to_full_map(self):
        dds_files = self.workspace.dds_files

        if not dds_files:
            raise exc.FolderIsEmpty(
                folder=Folder.CONVERTED,
                hint="Convert .ol files to .dds first"
            )

        self.parse_regions(dds_files)

        self.chunk_size = self._get_chunk_size()

        self.create_output_image()
        self.paste_regions()
        self.save_output_image()

    def parse_regions(self, dds_files: list[Path]):
        self.regions = RegionsList(
            [Region(dds) for dds in dds_files]
        )
        self.regions.sort()

    def create_output_image(self):
        size = self._get_output_image_size()

        self.output_image = Image.new(
            mode="RGB",
            size=size,
            color=MAP_BACKGROUND_COLOR
        )

    def paste_regions(self):
        print()
        print("🔗", "[b]Merging to full map...[/]")

        with FilesProgress(total=len(self.regions)) as progress:
            for region in self.regions:
                with Image.open(region.path) as img:
                    self.output_image.paste(img, self._get_image_coordinates(region))
                progress.increment()

    def save_output_image(self):
        print()
        print("📥", "[b]Saving image file...[/]")

        path = self.workspace.get_output_image_path()

        self.output_image.save(
            fp=path,
            compress_level=self.compress
        )

        print("🦄", f"[b purple]Image saved as[/] '{path}'[b purple].[/]")

    def _get_chunk_size(self):
        sizes = set()

        # Check that all images are square
        for region in self.regions:
            with Image.open(region.path) as img:
                size = ImgSize(img.width, img.height)

                if size.w != size.h:
                    raise exc.ImageIsNotSquare(size)

                sizes.add(size)

        # Check that all images have same resolution
        if len(sizes) != 1:
            raise exc.ImagesSizesNotSame(sizes)

        size = sizes.pop()
        return size.w

    def _get_output_image_size(self):
        w = (self.regions.width + 1) * self.chunk_size
        h = (self.regions.height + 1) * self.chunk_size

        size = ImgSize(w, h)

        resolution = size.w * size.h
        if resolution >= self.resolution_limit:
            raise exc.OutputImageTooLarge(size, self.resolution_limit)

        return size

    def _get_image_coordinates(self, region: Region):
        x = (region.x - self.regions.min_x) * self.chunk_size
        y = (region.z - self.regions.min_z) * self.chunk_size

        return Coords(x, y)
