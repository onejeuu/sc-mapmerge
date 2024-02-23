from InquirerPy import inquirer
from rich import print

from scmapmerge.consts import WorkspaceFolder as F
from scmapmerge.datatype import Confirm, Select


class Question:
    CLEAR_WORKSPACE = Confirm(
        message=f"Are you sure you want delete all files in {F.WORKSPACE} folder?",
        default=False,
    )

    SKIP_EMPTY_MAPS = Confirm(
        message=(
            "Files contain empty maps. Skip them?\n"
            "(Recommended, otherwise image may turn out too large)"
        ),
        default=True,
    )


def confirm(confirm: Confirm):
    print()
    return inquirer.confirm(message=confirm.message, default=confirm.default).execute()  # type: ignore


def select(select: Select):
    print()
    return inquirer.select(message=select.message, choices=select.choices).execute()  # type: ignore
