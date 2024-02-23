from typing import Optional

import click
from rich import print
from scfile.exceptions import ScFileException

from scmapmerge.consts import VERSION, Defaults
from scmapmerge.consts import WorkspaceFolder as F
from scmapmerge.datatype import Preset
from scmapmerge.enums import OutputFormat
from scmapmerge.exceptions import ScMapMergeException
from scmapmerge.image.output import OutputImage
from scmapmerge.merger import MapMerger
from scmapmerge.utils.asker import Question, confirm
from scmapmerge.utils.presets import PRESETS
from scmapmerge.utils.select_map import MapSelector
from scmapmerge.workspace import Workspace

from .params import PresetType
from .utils import join


@click.command()
@click.option(
    "-F",
    "--filename",
    nargs=1,
    default=Defaults.FILENAME,
    help="Output filename.",
    type=click.Path(exists=False, readable=True),
)
@click.option(
    "-S",
    "--suffix",
    nargs=1,
    default=Defaults.SUFFIX,
    help=f"Output format ({join(OutputFormat)}).",
    type=OutputFormat,
)
@click.option(
    "-P",
    "--preset",
    default=None,
    help=f"Output preset ({join(PRESETS)}).",
    type=PresetType(),
)
@click.option(
    "-L",
    "--limit",
    nargs=1,
    default=Defaults.RESOLUTION_LIMIT,
    help="Output resolution limit.",
    type=int,
)
@click.option("-D", "--clear", is_flag=True, help="Clear workspace folder.")
@click.option("-A", "--fromassets", is_flag=True, help="Select map from game assets.")
@click.option(
    "-N", "--nopause", is_flag=True, help="Removes pause before program exit."
)
@click.option(
    "--compress",
    default=Defaults.COMPRESS_LEVEL,
    help="Output compression level (png).",
    type=click.IntRange(0, 9, clamp=True),
)
@click.option(
    "--quality",
    default=Defaults.QUALITY,
    help="Output quality (jpg, webp).",
    type=click.IntRange(0, 100, clamp=True),
)
@click.option("--overwrite", is_flag=True, help="Overwrites an existing output image.")
@click.option("--debug", is_flag=True, help="Draws debug information on regions.")
def main(
    filename: str,
    suffix: str,
    preset: Optional[Preset],
    limit: int,
    clear: bool,
    nopause: bool,
    compress: int,
    quality: int,
    fromassets: bool,
    overwrite: bool,
    debug: bool,
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
            if confirm(Question.CLEAR_WORKSPACE):
                workspace.clear()
                print("\n[b yellow]Workspace has been successfully cleaned up.[/]")
            return

        if fromassets:
            selector = MapSelector()

            print(f"[b]Assets: '{selector.found.game}'[/]")

            path = selector.select_map()

            # it would be possible to read directly from game assets
            # but even though its slower, its safer
            workspace.clear_folder(F.ENCRYPTED)
            workspace.copy_files_to_encrypted(path)

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
            click.pause("\nPress Enter to exit...")
