from rich import print
from rich.prompt import Confirm

from scmapmerge.consts import Folder as F
from scmapmerge.datatype import Prompt


class Question:
    CLEAR_WORKSPACE = Prompt(
        message=(
            f"[b yellow]?[/] Are you sure you want "
            f"[b red]DELETE ALL[/] files in {F.WORKSPACE} folder?"
        ),
        default=False
    )

    SKIP_EMPTY_MAPS = Prompt(
        message=(
            "[b yellow]?[/] Files contain empty maps. Skip them?\n"
            "(Recommended, otherwise image may turn out too large)"
        ),
        default=True
    )


def ask(prompt: Prompt):
    print()
    return Confirm.ask(prompt.message, default=prompt.default)
