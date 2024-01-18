SC MAP MERGE
==========================

This CLI utility is designed to merging stalcraft map into single image.

You can use compiled executable from `Releases <https://github.com/onejeuu/sc-mapmerge/releases>`_ page.


💻 Usage
---------

Merge Map
~~~~~~~~~~~

1. Copy encrypted map files to ``workspace/1-encrypted`` folder.

    Map files end with ``.ol`` or ``.mic`` extension and are located in ``pda`` game assets folder.

    Folder ``workspace`` must be in same location as executable.

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

- ``-F`` ``--filename`` - Output filename. Defaults to ``Map %Y.%m.%d``. Accepts datetime formatting.

- ``-S`` ``--suffix`` - Output format. (``png``, ``jpg``, ``webp``, ``tiff``, ``bmp``, ``dds``). Defaults to ``jpg``.

- ``-P`` ``--preset`` - Output preset. (``zone``, ``newsever``).

- ``-L`` ``--limit`` - Output resolution limit, to prevent memory overflow. Defaults to ``1.000.000.000``.

- ``-D`` ``--clear`` - Clear workspace folder. Deletes all files.

- ``-N`` ``--nopause`` - Removes pause before program exit.

- ``--compress`` - Output compression level (``png``). From 0 to 9. Defaults to ``6``.

- ``--quality`` - Output quality % (``jpg``, ``webp``). From 0 to 100. Defaults to ``90``.

- ``--overwrite`` - Overwrites an existing output image.


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

Executable file will be created in ``/dist`` directory in your project folder.
