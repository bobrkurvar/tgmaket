from domain import Service


async def create(
    uow,
    service: Service,
) -> Service:
    async with uow:
        return await uow.generic.create(
            domain_obj=service,
        )


async def read(
    uow,
    **filters,
) -> tuple[Service, ...]:
    async with uow:
        return await uow.generic.read(
            Service,
            **filters,
        )