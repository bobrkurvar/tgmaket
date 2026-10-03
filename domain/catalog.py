from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Category:
    id: int
    name: str
    position: int


@dataclass
class Service:
    id: int
    category_id: int
    title: str
    short_description: str
    description: str
    price_from: Decimal
    image: str | None
    position: int