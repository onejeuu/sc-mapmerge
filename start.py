import argparse

from src.Merger import Merger


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--nodds", action="store_true", help="Не конвертировать в .dds")
    parser.add_argument("--nomap", action="store_true", help="Не объединять в карту")

    args = parser.parse_args()

    merger = Merger()

    if args.nodds and args.nomap:
        print()
        print("Nothind to do :3")

    if not args.nodds:
        merger.to_dds()

    if not args.nomap:
        merger.to_full_map()


if __name__ == "__main__":
    main()
