import click
from rich import print
from scfile.exceptions import ScFileException

from scmapmerge.asker import Asker
from scmapmerge.consts import VERSION, Defaults
from scmapmerge.exceptions import ScMapMergeException
from scmapmerge.merger import MapMerger
from scmapmerge.output import OutputImage
from scmapmerge.workspace import Workspace


@click.command()
@click.option(
    "-F", "--filename", nargs=1, default=Defaults.FILENAME,
    help="Output image filename prefix", type=click.Path(exists=False, readable=True)
)
@click.option(
    "-L", "--limit", nargs=1, default=Defaults.RESOLUTION_LIMIT,
    help="Output image resolution limit", type=int
)
@click.option(
    "-C", "--compress", default=Defaults.COMPRESS_LEVEL,
    help="PNG compression level", type=click.IntRange(0, 9)
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
    "--debug", is_flag=True,
    help="Draws debug information on regions"
)
def main(filename: str, limit: int, compress: int, clear: bool, nopause: bool, debug: bool):
    workspace = Workspace(filename)
    output = OutputImage(limit, compress, debug)
    asker = Asker(workspace)

    merger = MapMerger(workspace, output, asker)

    print("\n[b purple]STALCRAFT Map Merger[/]")
    print(f"[b]Version {VERSION}[/]")

    try:
        if clear:
            asker.clear_workspace()
            return

        merger.run()

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
