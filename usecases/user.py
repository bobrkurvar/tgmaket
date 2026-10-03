from domain import Seller, User


async def get_by_id(
    uow,
    telegram_id: int,
) -> User | Seller | None:
    async with uow:
        return await uow.generic.read_one(
            User,
            telegram_id=telegram_id,
        )


async def create_user(
    uow,
    user: User,
) -> User:
    async with uow:
        return await uow.generic.create(user)


async def create_seller(
    uow,
    seller: Seller,
) -> Seller:
    async with uow:
        return await uow.generic.create(seller)