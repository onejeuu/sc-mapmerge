from pathlib import Path
from typing import Optional

from rich import print
from scfile.utils import convert

from scmapmerge.consts import Folder as F
from scmapmerge.exceptions import PresetError
from scmapmerge.image.output import OutputImage
from scmapmerge.utils.asker import Question, ask
from scmapmerge.utils.presets import BasePreset
from scmapmerge.utils.progress import FilesProgress
from scmapmerge.utils.region import ConvertedRegions, EncryptedRegions
from scmapmerge.utils.workspace import Workspace


class MapMerger:
    def __init__(
        self,
        workspace: Workspace,
        output: OutputImage,
        preset: Optional[type[BasePreset]]
    ):
        self.workspace = workspace
        self.output = output
        self.preset = preset

    def merge(self) -> None:
        self.check_first_launch()
        self.workspace.create_folders()

        self.workspace.clear_folder(F.CONVERTED)
        self.convert_encrypted()

        self.merge_to_full_map()

    def check_first_launch(self) -> None:
        if not self.workspace.exists:
            self.workspace.create_folders()
            print(
                "\n[b yellow]Workspace has been successfully created.\n"
                "Place map files (.ol or .mic) in[/]"
                f"'{F.ENCRYPTED.as_posix()}' [b yellow]folder.[/]"
            )
            input("Press Enter to continue...")

    def convert_encrypted(self) -> None:
        encrypted = self.workspace.get_encrypted_files()
        regions = EncryptedRegions.from_pathes(encrypted)

        if self.preset:
            if not regions.contains_preset(self.preset.regions):
                raise PresetError()

            regions = regions.filter_preset(self.preset.regions)

        if regions.contains_empty() and ask(Question.SKIP_EMPTY_MAPS):
            # TODO: fix: empty maps may filter preset required regions
            regions = regions.filter_empty()

        self.convert_files(regions)

    def convert_files(self, regions: EncryptedRegions) -> None:
        # TODO: improve: quite ugly
        old_suffix = regions[0].path.suffix
        new_suffix = ".dds" if old_suffix == ".ol" else ".png"

        print()
        print("🔄", f"[b]Converting files to {new_suffix}...[/]")

        with FilesProgress(total=len(regions)) as progress:
            for region in regions:
                converted = Path(F.CONVERTED, region.path.with_suffix(new_suffix).name)
                convert.auto(region.path, converted)
                progress.increment()

    def merge_to_full_map(self) -> None:
        converted = self.workspace.get_converted_files()
        regions = ConvertedRegions.from_pathes(converted)
        regions.find_scale()

        self.output.create_image(regions)
        self.paste_regions(regions)
        self.crop_output_image()
        self.save_output_image()

    def paste_regions(self, regions: ConvertedRegions) -> None:
        print()
        print("🔗", "[b]Merging to full map...[/]")

        with FilesProgress(total=len(regions)) as progress:
            for region in regions:
                self.output.paste(region, regions)
                progress.increment()

    def crop_output_image(self) -> None:
        if self.preset and self.preset.crop:
            self.output.crop(self.preset.crop)

    def save_output_image(self) -> None:
        print()
        print("📥", "[b]Saving image file...[/]")

        path = self.workspace.output_image_path
        self.output.save(path)

        print("🦄", f"[b purple]Image saved as[/] '{path.as_posix()}'")
