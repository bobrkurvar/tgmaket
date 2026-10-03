from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import String, Text, Numeric, BigInteger
from decimal import Decimal

class Base(AsyncAttrs, DeclarativeBase):
    pass




class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
    )

    position: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )



class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    short_description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    price_from: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    image: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    position: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    username: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    type: Mapped[str]

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "buyer",
    }


class Admin(User):
    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }


class Seller(User):
    __tablename__ = "sellers"

    id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )

    rating: Mapped[Decimal | None] = mapped_column(
        Numeric(2, 1),
        nullable=True,
    )

    reviews_count: Mapped[int] = mapped_column(default=0)
    sales_count: Mapped[int] = mapped_column(default=0)

    __mapper_args__ = {
        "polymorphic_identity": "seller",
    }
