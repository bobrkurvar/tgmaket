from domain import Category


async def create(
    uow,
    category: Category,
) -> Category:
    async with uow:
        return await uow.db.create(
            domain_obj=category,
        )


async def read(
    uow,
    **filters,
) -> tuple[Category, ...]:
    async with uow:
        return await uow.db.read(
            Category,
            **filters,
        )