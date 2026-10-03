from domain import Category

async def get_catalog_data(
    uow,
    limit: int,
    offset: int = 0,
) -> tuple[tuple, int]:
    async with uow:
        categories = await uow.db.read(
            Category,
            is_active=True,
            offset=offset,
            limit=limit,
            order_by="position",
        )

        total = await uow.db.count(
            Category,
            is_active=True,
        )
    return categories, total