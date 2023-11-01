from pathlib import Path

import scfile
from PIL import Image
from rich import print

from scmapmerge import exceptions as exc
from scmapmerge.asker import Asker
from scmapmerge.consts import Folder, MapSettings, Prefix
from scmapmerge.progress import FilesProgress
from scmapmerge.region import Region, RegionsList
from scmapmerge.utils import Coords, ImgSize
from scmapmerge.workspace import Workspace


class MapMerger:
    def __init__(self):
        self.workspace = Workspace()
        self.workspace.prepare()

        self.asker = Asker(self.workspace)

    def run(self):
        self.asker.clear_converted()

        if not self.asker.skip_converting():
            self.convert_to_dds()

        self.merge_to_full_map()

    def convert_to_dds(self):
        ol_files = self.workspace.ol_files

        if not ol_files:
            raise exc.FolderIsEmpty(
                folder=Folder.ENCRYPTED,
                info="Put .ol files there"
            )

        if self.workspace.contains_empty_maps() and self.asker.skip_empty_maps():
            ol_files = self.workspace.not_empty_ol_files

        self.convert_ol_files(ol_files)

    def convert_ol_files(self, ol_files: list[Path]):
        print()
        print(Prefix.CONVERTING, "[b]Converting files to dds...[/]")

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
                info="Convert .ol files to .dds first"
            )

        self.parse_regions(dds_files)

        self.chunk_size = self._get_chunk_size()

        self.create_output_image()
        self.paste_regions()
        self.save_output_image()

    def parse_regions(self, dds_files: list[Path]):
        self.regions = RegionsList(
            *[Region(dds) for dds in dds_files]
        )
        self.regions.sort()

    def create_output_image(self):
        size = self._get_output_image_size()

        self.output_image = Image.new(
            mode="RGB",
            size=size,
            color=MapSettings.BACKGROUND_COLOR
        )

    def paste_regions(self):
        print()
        print(Prefix.MERGE, "[b]Merging to full map...[/]")

        with FilesProgress(total=len(self.regions)) as progress:
            for region in self.regions:
                with Image.open(region.path) as img:
                    self.output_image.paste(img, self._get_image_coordinates(region))
                progress.increment()

    def save_output_image(self):
        print()
        print(Prefix.SAVE, "[b]Saving image file...[/]")

        self.output_image.save(f"{Folder.OUTPUT}/{MapSettings.FILENAME}.png")

        print(Prefix.OUTPUT, f"[b purple]Image saved to[/] '{Folder.OUTPUT.as_posix()}' [b purple]folder.[/]")

    def _get_chunk_size(self):
        sizes = {
            ImgSize(w=img.width, h=img.height)
            for region in self.regions
            for img in [Image.open(region.path)]
        }

        if len(sizes) != 1:
            raise exc.ImagesSizesNotSame("Map images should be the same size")

        size = sizes.pop()
        if size.w != size.h:
            raise exc.ImageIsNotSquare("Map images should be square")

        return size.w

    def _get_output_image_size(self):
        size = ImgSize(
            w=(self.regions.width + 1) * self.chunk_size,
            h=(self.regions.height + 1) * self.chunk_size
        )

        resolution = size.w * size.h

        if resolution >= MapSettings.RESOLUTION_LIMIT:
            raise exc.ImageResolutionLimit(
                f"Output image is to big - {size.w}px x {size.h}px"
            )

        return size

    def _get_image_coordinates(self, region: Region):
        x = (region.x - self.regions.min_x) * self.chunk_size
        y = (region.z - self.regions.min_z) * self.chunk_size

        return Coords(x, y)
