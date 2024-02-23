from pathlib import Path
from typing import Optional

import click
from rich import print
from scfile.utils import convert

from scmapmerge.consts import OutputFile
from scmapmerge.consts import WorkspaceFolder as F
from scmapmerge.datatype import Preset
from scmapmerge.image import BaseOutputImage
from scmapmerge.merger.exceptions import MissingRegions
from scmapmerge.region.listing.converted import ConvertedRegions
from scmapmerge.region.listing.encrypted import EncryptedRegions
from scmapmerge.utils.asker import Question, confirm
from scmapmerge.utils.progress import FilesProgress
from scmapmerge.workspace.base import BaseWorkspace

from .base import BaseMapMerger


class MapMerger(BaseMapMerger):
    def __init__(
        self,
        workspace: BaseWorkspace,
        output: BaseOutputImage,
        preset: Optional[Preset],
    ):
        self.workspace = workspace
        self.output = output
        self.preset = preset

    def merge(self) -> None:
        self.check_first_launch()
        self.workspace.create()

        self.workspace.clear_folder(F.CONVERTED)
        self.convert_encrypted()

        self.merge_to_full_map()

    def check_first_launch(self) -> None:
        """Create workspace if it's first launch."""

        if not self.workspace.exists:
            self.workspace.create()
            print(
                "\n[b yellow]Workspace has been successfully created.\n"
                "Copy encrypted map files (.ol or .mic) to[/] "
                f"'{F.ENCRYPTED.as_posix()}' [b yellow]folder.[/]"
            )
            click.pause("Press Enter to continue...")

    def convert_encrypted(self) -> None:
        """Prepares encrypted regions list."""

        encrypted = self.workspace.get_encrypted_files()
        regions = EncryptedRegions.from_paths(encrypted)
        regions.preset = self.preset

        self.filter_preset(regions)
        self.filter_empty(regions)
        self.warn_about_alpha(regions)
        self.convert_files(regions)

    def filter_preset(self, regions: EncryptedRegions):
        if self.preset:
            if not regions.contains_preset:
                raise MissingRegions(self.preset.name, regions.missing_preset)

            regions.filter_preset()

    def filter_empty(self, regions: EncryptedRegions):
        if regions.contains_empty and confirm(Question.SKIP_EMPTY_MAPS):
            regions.filter_empty()

    def warn_about_alpha(self, regions: EncryptedRegions):
        """Warns if output format does not support alpha and regions is overlay"""

        if (
            regions.possible_overlay
            and self.output.format in OutputFile.NONTRANSPARENT_FORMATS
        ):
            print()
            print(
                "[b][yellow]Output possibly is overlay, but "
                f"selected suffix ({self.output.format}) does not support transparency.[/]"
            )

    def convert_files(self, regions: EncryptedRegions) -> None:
        """Convert encrypted map files."""

        print()
        print("🔄", f"[b]Converting regions to {regions.new_suffix}...[/]")

        with FilesProgress(total=len(regions)) as progress:
            for region in regions:
                convert.auto(
                    region.path,
                    Path(F.CONVERTED, region.get_new_filename(regions.new_suffix)),
                )
                progress.increment()

    def merge_to_full_map(self) -> None:
        """Prepares converted regions list."""

        converted = self.workspace.get_converted_files()
        regions = ConvertedRegions.from_paths(converted)
        regions.find_scale()

        self.output.regions = regions
        self.output.create()

        self.paste_regions(regions)
        self.crop_output()
        self.save_output()

    def paste_regions(self, regions: ConvertedRegions) -> None:
        """Paste regions images onto output image."""

        print()
        print("🔗", "[b]Merging to full map...[/]")

        with FilesProgress(total=len(regions)) as progress:
            for region in regions:
                self.output.paste(region)
                progress.increment()

    def crop_output(self) -> None:
        if self.preset and self.preset.crop:
            self.output.crop(self.preset.crop)

    def save_output(self) -> None:
        print()
        print("📥", "[b]Saving image file...[/]")

        path = self.workspace.get_output_image_path()
        self.output.save(path)

        print("🦄", f"[b purple]Image saved as[/] '{path.as_posix()}'")
