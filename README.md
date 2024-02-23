# SC MAP MERGE

This CLI utility is designed to merging stalcraft map into single image.

You can use compiled executable from [Releases](https://github.com/onejeuu/sc-mapmerge/releases) page.


## 💻 Usage

### Merge Map

1. Copy encrypted map files.

    Copy files with `.ol` or `.mic` extension to `workspace/1-encrypted` folder.

    Folder `workspace` must be in same location as `scmapmerge.exe`.

    Map files located in `pda` folder of game assets.

2. Run `scmapmerge.exe`.

> [!TIP]
> You can use `--fromassets` flag to select map without manual copying.

### Workspace

#### Create

- Run `scmapmerge.exe`. Workspace folders will be created automatically.

#### Clear

- Delete `workspace` folder.

    or

- Run `scmapmerge.exe` with `-D` or `--clear` flag.

    This will delete **all files** in `workspace` folder, including `workspace/3-output`.

### Options

- `--help` Show help message.

- `-F`, `--filename` - Output filename. Accepts [datetime formatting](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes). Defaults to `"Map %Y.%m.%d"`.

- `-S`, `--suffix` - Output format. (`png`, `jpg`, `webp`, `tiff`, `bmp`, `dds`). Defaults to jpg.

- `-P`, `--preset` - Output preset. (`zone`, `newsever`, `underpd`, ...). Defaults to None.

- `-L`, `--limit` - Output resolution limit, to prevent memory overflow. Specify 0 to ignore.

- `--compress` - Output compression level (png). From 0 to 9. Defaults to 6.

- `--quality` - Output quality % (jpg, webp). From 0 to 100. Defaults to 90.

### Flags

- `-D`, `--clear` - Clear workspace folder. Deletes all files.

- `-A`, `--fromassets` - Select map from game assets. No need to manually copy files.

- `-N`, `--nopause` - Removes pause before program exit.

- `--overwrite` - Overwrites an existing output image.

### Example

```bash
scmapmerge -N -F "Map" -S jpg -P zone --quality 100 --overwrite
```


## 🛠️ Build

> [!IMPORTANT]
> You will need **poetry** to compile. Install it from [here](https://python-poetry.org).

> [!TIP]
> Before proceeding, it's recommended to create virtual environment
>
> ```bash
> poetry shell
> ```

Then install dependencies:

```bash
poetry install
```

And run script to compile:

```bash
poetry run build
```

Executable file will be created in `/dist` directory in your project folder.
