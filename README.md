# SC MAP MERGE

This CLI utility is designed to merging stalcraft map into single image.

You can use compiled executable from [Releases](https://github.com/onejeuu/sc-mapmerge/releases) page.


## 💻 Usage

### Merge Map

1. Copy encrypted map files to `workspace/1-encrypted` folder.

> [!IMPORTANT]
> Folder `workspace` must be in same location as `scmapmerge.exe`.

> [!NOTE]
> Map files end with `.ol` or `.mic` extension and located in `pda` game assets folder.

2. Run `scmapmerge.exe`.

### Create Workspace

- Run `scmapmerge.exe`. Workspace folders will be created automatically.

### Clear Workspace

- Delete `workspace` folder.

or

- Run `scmapmerge.exe` with `-D` or `--clear` flag.

> [!WARNING]
> This will delete **all files** in `workspace` folder, including `workspace/3-output`.

### Options

- `--help` Show help message.

- `-F` `--filename` - Output filename. Accepts [datetime formatting](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes). Defaults to `"Map %Y.%m.%d"`.

- `-S` `--suffix` - Output format. (`png`, `jpg`, `webp`, `tiff`, `bmp`, `dds`). Defaults to jpg.

- `-P` `--preset` - Output preset. (`zone`, `newsever`, `underpd`, ...). Defaults to None.

- `-L` `--limit` - Output resolution limit, to prevent memory overflow. Defaults to 1.000.000.000.

- `--compress` - Output compression level (png). From 0 to 9. Defaults to 6.

- `--quality` - Output quality % (jpg, webp). From 0 to 100. Defaults to 90.

### Flags

- `-D` `--clear` - Clear workspace folder. Deletes all files.

- `-N` `--nopause` - Removes pause before program exit.

- `--overwrite` - Overwrites an existing output image.

### Example

```bash
scmapmerge -F "Map" -S jpg -P zone --quality 100 -N --overwrite
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
