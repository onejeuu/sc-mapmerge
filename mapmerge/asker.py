from typing import NamedTuple

from rich.prompt import Confirm

from mapmerge.workspace import Workspace
from mapmerge.consts import Prefix, Folder


class Asker:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    @classmethod
    def clear_workspace(cls):
        print()
        return Confirm.ask(Prompt.CLEAR_WORKSPACE, default=Default.CLEAR_WORKSPACE)

    def clear_converted(self):
        if not self.workspace.is_empty(Folder.CONVERTED):
            print()
            if Confirm.ask(Prompt.CLEAR_CONVERTED, default=Default.CLEAR_CONVERTED):
                self.workspace.clear(Folder.CONVERTED)

    def skip_converting(self):
        if not self.workspace.is_empty(Folder.CONVERTED):
            print()
            return Confirm.ask(Prompt.SKIP_CONVERTING, default=Default.SKIP_CONVERTING)

    def skip_empty_maps(self):
        print()
        return Confirm.ask(Prompt.SKIP_EMPTY_MAPS, default=Default.SKIP_EMPTY_MAPS)


class Prompt(NamedTuple):
    CLEAR_WORKSPACE = (
        f"{Prefix.QUESTION} Are you sure you want "
        f"[b red]DELETE ALL[/] files in {Folder.WORKSPACE} folder?"
    )
    CLEAR_CONVERTED = (
        f"{Prefix.QUESTION} \"{Folder.CONVERTED.name}\" folder is not empty. "
        "Clean it up?"
    )
    SKIP_CONVERTING = f"{Prefix.QUESTION} Skip step converting to .dds?"
    SKIP_EMPTY_MAPS = (
        f"{Prefix.QUESTION} Files contains empty maps. Skip them?\n"
        "(Strictly recommended, otherwise image can turn out incredibly large)"
    )


class Default(NamedTuple):
    CLEAR_WORKSPACE = False
    CLEAR_CONVERTED = False
    SKIP_CONVERTING = True
    SKIP_EMPTY_MAPS = True
