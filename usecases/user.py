from domain import Seller, User


async def get_by_id(
    uow,
    telegram_id: int,
) -> User | Seller | None:
    async with uow:
        return await uow.db.read_one(
            User,
            telegram_id=telegram_id,
        )


async def create_user(
    uow,
    user: User,
) -> User:
    async with uow:
        return await uow.db.create(user)


async def create_seller(
    uow: UnitOfWork,
    seller: Seller,
) -> Seller:
    async with uow:
        return await uow.db.create(seller)