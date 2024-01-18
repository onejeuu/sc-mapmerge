from typing import Optional

import click
from rich import print
from scfile.exceptions import ScFileException

from scmapmerge.consts import VERSION, Defaults
from scmapmerge.enums import OutputSuffix
from scmapmerge.exceptions import ScMapMergeException
from scmapmerge.image.output import OutputImage
from scmapmerge.merger import MapMerger
from scmapmerge.utils.asker import Question, ask
from scmapmerge.utils.presets import PRESETS, BasePreset
from scmapmerge.utils.workspace import Workspace


PRESET_NAMES = ", ".join(preset.name for preset in PRESETS)


class PresetType(click.ParamType):
    name = "preset"

    def convert(self, value, param, ctx):
        for preset in PRESETS:
            if value == preset.name:
                return preset
        self.fail(f"Invalid preset: {value}. Available presets are: {PRESET_NAMES}", param, ctx)


@click.command()
@click.option(
    "-F", "--filename", nargs=1, default=Defaults.FILENAME,
    help="Output filename", type=click.Path(exists=False, readable=True)
)
@click.option(
    "-S", "--suffix", nargs=1, default=Defaults.SUFFIX,
    help="Output format", type=OutputSuffix
)
@click.option(
    "-P", "--preset", default=None,
    help=f"Output preset ({PRESET_NAMES})", type=PresetType()
)
@click.option(
    "-L", "--limit", nargs=1, default=Defaults.RESOLUTION_LIMIT,
    help="Output resolution limit", type=int
)
@click.option(
    "-D", "--clear", is_flag=True,
    help="Clear workspace folder"
)
@click.option(
    "-N", "--nopause", is_flag=True,
    help="Removes pause before program exit"
)
@click.option(
    "--compress", default=Defaults.COMPRESS_LEVEL,
    help="Output compression level (png)", type=click.IntRange(0, 9)
)
@click.option(
    "--quality", default=Defaults.QUALITY,
    help="Output quality (jpg, webp)", type=click.IntRange(0, 100)
)
@click.option(
    "--overwrite", is_flag=True,
    help="Overwrites an existing output image"
)
@click.option(
    "--debug", is_flag=True,
    help="Draws debug information on regions"
)
def main(
    filename: str,
    suffix: str,
    preset: Optional[type[BasePreset]],
    limit: int,
    clear: bool,
    nopause: bool,
    compress: int,
    quality: int,
    overwrite: bool,
    debug: bool
):
    workspace = Workspace(filename, suffix, overwrite)
    output = OutputImage(suffix, limit, compress, quality, debug)

    merger = MapMerger(workspace, output, preset)

    print("\n[b purple]STALCRAFT Map Merger[/]")
    print(f"[b]Version: {VERSION}[/]")

    if preset:
        print(f"[b]Preset: '{preset.name}'[/]")

    if debug:
        print(f"[b]Debug: {debug}[/]")

    try:
        if clear:
            if ask(Question.CLEAR_WORKSPACE):
                workspace.clear_all_folders()
                print("\n[b yellow]Workspace has been successfully cleaned up.[/]")
            return

        merger.merge()

    except ScMapMergeException as err:
        print(f"\n[b red]Error:[/] {err}")

    except ScFileException as err:
        print(f"\n[b red]Unable to convert map file:[/] {err}")

    except Exception as err:
        print(f"\n[b red]Unknown Error:[/] {err}")

    except KeyboardInterrupt:
        print("\n\n[b yellow]Operation aborted.[/]")

    finally:
        if not nopause:
            input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
