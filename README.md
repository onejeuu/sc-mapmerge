# Sc Map Merge

This CLI utility is designed to merging stalcraft map into single image.

You can use compiled executable from [Releases](https://github.com/onejeuu/sc-mapmerge/releases/) page.

## Usage

### Merge Map

1. Put encrypted map files in `workspace/1-encrypted` folder.

    Map files end with the `.ol` extension and are located in `pda` game assets folder.

    Folder `workspace` must be in same location as compiled utility.

2. Run utility.

### Create Workspace

Run utility. Folders will be created automatically.

### Clear Workspace

Run utility with `--clear` or `-D` option.

This will delete absolutely **all files** in workspace folder, including **`workspace/3-output`**.


## Build
```console
poetry install
```

```console
poetry run build
```
