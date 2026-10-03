from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Catalog(Generic[T]):
    content: tuple[T, ...]
    total: int