from pathlib import Path

from rich import print
from scfile.utils import convert

from scmapmerge.asker import Asker
from scmapmerge.consts import Folder as F
from scmapmerge.image.output import OutputImage
from scmapmerge.utils.progress import FilesProgress
from scmapmerge.utils.region import Region, RegionsList
from scmapmerge.utils.workspace import Workspace


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

    def merge(self) -> None:
        self.check_first_launch()
        self.workspace.create_folders()

        self.asker.clear_converted()

        if not self.asker.skip_converting():
            self.convert_encrypted()

        self.merge_to_full_map()

    def check_first_launch(self) -> None:
        if not self.workspace.exists:
            self.workspace.create_folders()
            print(
                "\n[b yellow]Workspace has been successfully created.\n"
                f"Place map files (.ol or .mic) in[/] '{F.ENCRYPTED.as_posix()}' [b yellow]folder.[/]"
            )
            input("Press Enter to continue...")

    def convert_encrypted(self) -> None:
        encrypted = self.workspace.get_encrypted_files()

        if self.workspace.contains_empty_maps() and self.asker.skip_empty_maps():
            encrypted = self.workspace.filter_empty_maps(encrypted)

        self.convert_files(encrypted)

    def convert_files(self, encrypted: list[Path]) -> None:
        old_suffix = encrypted[0].suffix
        new_suffix = ".dds" if old_suffix == ".ol" else ".png"

        print()
        print("🔄", f"[b]Converting files to {new_suffix}...[/]")

        with FilesProgress(total=len(encrypted)) as progress:
            for path in encrypted:
                converted = Path(F.CONVERTED, path.with_suffix(new_suffix).name)
                convert.auto(path, converted)
                progress.increment()

    def merge_to_full_map(self) -> None:
        converted = self.workspace.get_converted_files()

        regions = RegionsList([Region(dds) for dds in converted])

        self.output.create_image(regions)
        self.paste_regions(regions)
        self.save_output_image()

    def paste_regions(self, regions: RegionsList) -> None:
        print()
        print("🔗", "[b]Merging to full map...[/]")

        with FilesProgress(total=len(regions)) as progress:
            for region in regions:
                self.output.paste(region, regions)
                progress.increment()

    def save_output_image(self) -> None:
        print()
        print("📥", "[b]Saving image file...[/]")

        path = self.workspace.get_output_image_path()
        self.output.save(path)

        print("🦄", f"[b purple]Image saved as[/] '{path}'")
