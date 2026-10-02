from domain import Service


async def create(
    uow,
    service: Service,
) -> Service:
    async with uow:
        return await uow.db.create(
            domain_obj=service,
        )


async def read(
    uow,
    **filters,
) -> tuple[Service, ...]:
    async with uow:
        return await uow.db.read(
            Service,
            **filters,
        )