from pathlib import Path

import scfile
from PIL import Image
from rich import print

from scmapmerge import exceptions as exc
from scmapmerge.asker import Asker
from scmapmerge.consts import Folder
from scmapmerge.output import OutputImage
from scmapmerge.progress import FilesProgress
from scmapmerge.region import Region, RegionsList
from scmapmerge.workspace import Workspace


class MapMerger:
    def __init__(
        self,
        workspace: Workspace,
        output: OutputImage,
        asker: Asker
    ):
        self.workspace = workspace
        self.output = output
        self.asker = asker

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
                f"Place .ol map files in[/] '{Folder.ENCRYPTED.as_posix()}' [b yellow]folder.[/]"
            )
            input("Press Enter to continue...")

    def convert_to_dds(self):
        ol_files = self.workspace.ol_files

        if not ol_files:
            raise exc.FolderIsEmpty(Folder.ENCRYPTED, "Put .ol map files there")

        if self.workspace.contains_empty_maps() and self.asker.skip_empty_maps():
            ol_files = self.workspace.not_empty_ol_files

        self.convert_ol_files(ol_files)

    def convert_ol_files(self, ol_files: list[Path]):
        print()
        print("🔄", "[b]Converting files to dds...[/]")

        with FilesProgress(total=len(ol_files)) as progress:
            for ol in ol_files:
                dds = Path(Folder.CONVERTED, ol.with_suffix(".dds").name)
                scfile.ol_to_dds(ol, dds)
                progress.increment()

    def merge_to_full_map(self):
        dds_files = self.workspace.dds_files

        if not dds_files:
            raise exc.FolderIsEmpty(Folder.CONVERTED, "Convert .ol files to .dds first")

        regions = RegionsList([Region(dds) for dds in dds_files])
        regions.sort()

        self.output.create(regions)

        self.paste_regions(regions)

        self.save_output_image()

    def paste_regions(self, regions: RegionsList):
        print()
        print("🔗", "[b]Merging to full map...[/]")

        with FilesProgress(total=len(regions)) as progress:
            for region in regions:
                with Image.open(region.path) as img:
                    self.output.paste(img, region, regions)
                progress.increment()

    def save_output_image(self):
        print()
        print("📥", "[b]Saving image file...[/]")

        path = self.workspace.get_output_image_path()

        self.output.save(path)

        print("🦄", f"[b purple]Image saved as[/] '{path}'")
