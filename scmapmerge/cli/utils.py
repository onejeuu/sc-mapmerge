from typing import Any, Iterable


def join(items: Iterable[Any]):
    return ", ".join(str(item) for item in items)
