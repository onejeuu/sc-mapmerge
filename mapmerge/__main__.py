import argparse

from rich import print

from mapmerge import exceptions as exc
from mapmerge.merger import MapMerger


def error(text: str):
    print()
    print(f"[b red]Error:[/] {text}")


def main():
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    merger = MapMerger()

    try:
        merger.run()

    except exc.FolderIsEmpty as err:
        error(f"Folder '{err.folder}' has no .ol files!")

    except exc.ScFileError as err:
        error(f"Unable to convert .ol file '{err.filename}'")

    except Exception as err:
        error(f"Unknown error - {err}")

    except KeyboardInterrupt:
        print()
        print()
        print("[b yellow]Operation aborted.[/]")


if __name__ == "__main__":
    main()
