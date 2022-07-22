import json
from collections import defaultdict
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Callable, DefaultDict, Iterator, TypeVar

from pydantic.json import pydantic_encoder

T = TypeVar("T")
G = TypeVar("G")


def json_dumps(data: Any) -> str:
    return json.dumps(data, default=pydantic_encoder)


def json_loads(raw: str) -> Any:
    return json.loads(raw)


def group_by(items: list[T], key: Callable[[T], G]) -> DefaultDict[G, list[T]]:
    """Group item by key func"""

    mapping: DefaultDict[G, list[T]]
    mapping = defaultdict(list)
    for item in items:
        mapping[key(item)].append(item)
    return mapping


@contextmanager
def set_context_var(var: ContextVar[T], value: T) -> Iterator[None]:
    token = var.set(value)
    try:
        yield
    finally:
        var.reset(token)
