import os
from pathlib import Path

from PIL import Image
from rich import print

from src.Consts import BACKGROUND_COLOR, FILENAME, FOLDER, PIXELS_LIMIT, VERSION
from src.Files import OlFile
from src.Formats import Format
from src.LoadingBar import LoadingBar
from src.Region import Region
from src.Utils import BlockMaxCoords, BlockMinCoords, ImageSize


class Merger:
    def __init__(self):
        self.image_size = ImageSize()

        self.min_coords = BlockMinCoords()
        self.max_coords = BlockMaxCoords()

        self.block_size = 512
        self.block_sizes = []

        self.output_image: Image.Image

        self._startup()

    def _startup(self):
        print("[b][purple]STALCRAFT MAP MERGER[/]")
        print("[b][purple]Version:[/]", VERSION)

        for folder in (FOLDER.ORIGINAL, FOLDER.CONVERTED, FOLDER.OUTPUT):
            path = Path(Path.cwd(), folder)
            path.mkdir(exist_ok=True)

    def _find_min_and_max(self, dds_files):
        list_x = [Region(filename).x for filename in dds_files]
        list_z = [Region(filename).z for filename in dds_files]

        self.min_coords.x = min(list_x)
        self.min_coords.z = min(list_z)

        self.max_coords.x = max(list_x)
        self.max_coords.z = min(list_z)

    def _find_image_size(self, dds_files):
        files_by_x = {}

        for filename in dds_files:
            x = int(Region(filename).x)

            if x not in files_by_x:
                files_by_x[x] = [filename]
            else:
                files_by_x[x].append(filename)

        width = len(set([Region(filename).x for filename in dds_files]))
        height = len(set([
            Region(filename).z
            for filenames in files_by_x.values()
            for filename in filenames
        ]))

        self.image_size.width = width * self.block_size
        self.image_size.height = height * self.block_size

    def _check_block_sizes(self):
        unique_sizes = set(self.block_sizes)

        if len(unique_sizes) > 1:
            print()
            print("❗", "[red]Images are not the same size:[/]", unique_sizes)
            input()
            return False

        if not all(len(set(tup)) == 1 for tup in self.block_sizes):
            print()
            print("❗", "[red]Images are not square:[/]", unique_sizes)
            input()
            return False

        self.block_size: int = self.block_sizes[0][0]

        return True

    def _update_region(self):
        Region.BLOCK_SIZE = self.block_size # type: ignore
        Region.IMAGE_SIZE = self.image_size
        Region.MIN = self.min_coords
        Region.MAX = self.max_coords

    def _create_new_image(self):
        self.output_image = Image.new(
            mode = "RGB",
            size = (
                self.image_size.width,
                self.image_size.height
            ),
            color = BACKGROUND_COLOR
        )

    def _unique_colors(self, path):
        image = Image.open(path).convert("RGB")
        pixels = image.getdata()
        return len(set(pixels))

    def to_dds(self):
        print()
        print("🔄", "[yellow]Converting to dds...[/]")

        input_folder = FOLDER.ORIGINAL
        output_folder = FOLDER.CONVERTED

        files = os.listdir(input_folder)
        ol_files = [f for f in files if f.endswith(Format.OL)]

        if not files:
            print("❗", "[red]Folder[/]", f'"{input_folder}"', "[red]is empty.[/]")
            return

        loading_bar = LoadingBar("⏳", max=len(files))

        for filename in ol_files:
            input_path = Path(Path.cwd(), input_folder, filename)
            output_path = Path(Path.cwd(), output_folder, f"{input_path.stem}{Format.DDS}")

            self.block_sizes.append(
                OlFile(input_path, output_path).convert()
            )

            loading_bar.next()

        loading_bar.finish()
        print("✅", "[b][green]Done.[/]")

    def to_full_map(self):
        if not self._check_block_sizes():
            return

        print()
        print("🔗", "[yellow]Merging to full map...[/]")

        input_folder = FOLDER.CONVERTED
        output_folder = FOLDER.OUTPUT

        files = os.listdir(input_folder)

        if not files:
            print("❗", "[red]Folder[/]", f'"{input_folder}"', "[red]is empty.[/]")
            return

        dds_files = [f for f in files if f.endswith(Format.DDS)]
        dds_files.sort(key=lambda filename: (Region(filename).x, Region(filename).z))

        clear_dds_files = dds_files

        '''
        clear_dds_files = []

        for filename in dds_files:
            if self._unique_colors(f"{input_folder}/{filename}") > 30:
                clear_dds_files.append(filename)
        '''

        self._find_min_and_max(clear_dds_files)
        self._find_image_size(clear_dds_files)

        self._update_region()

        image_pixels = self.image_size.width * self.image_size.height

        if image_pixels > PIXELS_LIMIT:
            print()
            print("❗", "[red]Output image is too big:[/]", self.image_size.width, "x", self.image_size.height)
            return

        self._create_new_image()

        loading_bar = LoadingBar("⏳", max=len(dds_files))

        print("Image size:", self.image_size.width, "x", self.image_size.height)
        print("Min coords:", "x", "-", self.min_coords.x, "z", "-", self.min_coords.z)
        print("Max coords:", "x", "-", self.max_coords.x, "z", "-", self.max_coords.z)
        print("Block size:", self.block_size)
        print()

        for filename in clear_dds_files:
            region = Region(filename)

            with Image.open(f"{input_folder}/{filename}") as img:
                coordinates = region.coordinates
                self.output_image.paste(img, (coordinates.x, coordinates.z))

            loading_bar.next()

        loading_bar.finish()
        print("✅", "[b][green]Done.[/]")

        print()
        print("📥", "[yellow]Saving file...[/]")

        self.output_image.save(f"{output_folder}/{FILENAME}.png")

        print()
        print("🖼", f"[b][purple]Image saved in[/] '{output_folder}' [b][purple]folder.[/]")

        print()
        input("Press Enter to exit...")
