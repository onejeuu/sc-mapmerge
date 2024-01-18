SC MAP MERGE
==========================

This CLI utility is designed to merging stalcraft map into single image.

You can use compiled executable from `Releases <https://github.com/onejeuu/sc-mapmerge/releases>`_ page.


💻 Usage
---------

Merge Map
~~~~~~~~~~~

1. Copy encrypted map files in ``workspace/1-encrypted`` folder.

    Map files end with ``.ol`` or ``.mic`` extension and are located in ``pda`` game assets folder.

    Folder ``workspace`` must be in same location as utility.

2. Run executable.

Create Workspace
~~~~~~~~~~~~~~~~~

- Run utility. Folders will be created automatically.

Clear Workspace
~~~~~~~~~~~~~~~~

- Delete ``workspace`` folder.

or

- Run utility with ``-D`` or ``--clear`` option.

    This will delete **all files** in ``workspace`` folder, including ``workspace/3-output``.

Options
~~~~~~~~

- ``--help`` Show help message.

- ``-F`` ``--filename`` - Output filename. Defaults to "Map %Y.%m.%d". Accepts datetime formatting.

- ``-S`` ``--suffix`` - Output format. (png, jpg, webp, bmp, dds). Defaults to jpg.

- ``-P`` ``--preset`` - Output preset. (zone, newsever).

- ``--limit`` - Output resolution limit, to prevent memory overflow.

- ``--compress`` - Output compression level (png). From 0 to 9. Defaults to 6.

- ``--quality`` - Output quality % (jpg, webp). From 0 to 100. Defaults to 90.

- ``--overwrite`` - Overwrite output image if exists.

- ``-D`` ``--clear`` - Clear workspace folder. Deletes all files.

- ``-N`` ``--nopause`` - Removes pause before program exit.


🛠️ Build
---------

You will need poetry to do compilation. Install it `here <https://python-poetry.org>`_.

Before proceeding, it's recommended to create virtual environment:

.. code:: bash

    poetry shell

Then install dependencies:

.. code:: bash

    poetry install

And run script to compile:

.. code:: bash

    poetry run build

Executable file will be created in ``/dist`` directory within your project folder.
