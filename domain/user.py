from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class User:
    username: str | None
    id: int | None = None


@dataclass(slots=True)
class Admin(User):
    pass


@dataclass(slots=True)
class Seller(User):
    rating: Decimal | None = None
    reviews_count: int = 0
    sales_count: int = 0