from dataclasses import dataclass

from rich import print
from rich.prompt import Confirm

from scmapmerge.consts import Folder as F
from scmapmerge.utils.workspace import Workspace


@dataclass
class Prompt:
    question: str
    default: bool


CLEAR_WORKSPACE = Prompt(
    question=(
        f"[b yellow]?[/] Are you sure you want "
        f"[b red]DELETE ALL[/] files in {F.WORKSPACE} folder?"
    ),
    default=False
)

CLEAR_CONVERTED = Prompt(
    question=f"[b yellow]?[/] '{F.CONVERTED.as_posix()}' is not empty. Clean it up?",
    default=False
)

SKIP_CONVERTING = Prompt(
    question="[b yellow]?[/] Skip converting step?",
    default=True
)

SKIP_EMPTY_MAPS = Prompt(
    question=(
        "[b yellow]?[/] Files contain empty maps. Skip them?\n"
        "(Recommended, otherwise image may turn out too large)"
    ),
    default=True
)


def ask(prompt: Prompt):
    print()
    return Confirm.ask(prompt.question, default=prompt.default)


class Asker:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    def clear_workspace(self) -> None:
        if ask(CLEAR_WORKSPACE):
            self.workspace.clear_all_folders()
            print("\n[b yellow]Workspace has been successfully cleaned up.[/]")

    def clear_converted(self) -> None:
        if not self.workspace.is_empty(F.CONVERTED) and ask(CLEAR_CONVERTED):
            self.workspace.clear_folder(F.CONVERTED)

    def skip_converting(self) -> bool:
        if not self.workspace.is_empty(F.CONVERTED):
            return ask(SKIP_CONVERTING)
        return False

    def skip_empty_maps(self) -> bool:
        return ask(SKIP_EMPTY_MAPS)
