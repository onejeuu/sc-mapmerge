import argparse

from rich import print
from scfile.exceptions import ScFileException

from scmapmerge import exceptions as exc
from scmapmerge.merger import MapMerger
from scmapmerge.asker import Asker
from scmapmerge.consts import VERSION


def error(text: str):
    print()
    print(f"[b red]Error:[/] {text}")


def info(text: str):
    print()
    print(f"[b yellow]{text}[/]")


def title():
    print()
    print("[b purple]STALCRAFT Map Merger[/]")
    print(f"[b]Version {VERSION}[/]")


def pause():
    print()
    input("Press Enter to exit...")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-clear", action="store_true", help="Clear workspace")

    args = parser.parse_args()

    merger = MapMerger()

    title()

    try:
        if args.clear:
            if Asker.clear_workspace():
                merger.workspace.clear_all()
                info("Workspace has been successfully cleaned up.")
            return

        merger.run()

    except exc.FolderIsEmpty as err:
        error(f"'{err.folder.as_posix()}' folder has no required files. {err.info}.")

    except exc.ImageResolutionLimit as err:
        error(str(err))

    except ScFileException as err:
        error(f"Unable to convert .ol file - {err}.")

    except Exception as err:
        error(f"Unknown error - {err}.")

    except KeyboardInterrupt:
        print()
        info("Operation aborted.")


if __name__ == "__main__":
    main()
    pause()
