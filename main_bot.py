import asyncio
import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from core import setup_logging, conf
from adapters.redis import RedisProvider, RedisService
from handlers import main_router
from adapters.db_provider import DbProvider
from adapters.uow import UnitOfWork
from db.mapper import registry


bot = Bot(conf.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
log = logging.getLogger(__name__)

setup_logging()

@asynccontextmanager
async def init_all():
    redis_provider = db_provider = None
    try:
        redis_provider = await RedisProvider.create(conf.redis_url)
        redis_conn = redis_provider.conn
        redis_service = RedisService(prefix="front", redis=redis_conn)
        storage = RedisStorage(redis=redis_conn, state_ttl=3600)
        db_provider = DbProvider(url=conf.db_url)
        uow = UnitOfWork(provider=db_provider, registry=registry)
        dp = Dispatcher(storage=storage)
        dp["redis_service"] = redis_service
        dp["uow"] = uow
        dp.include_router(main_router)
        log.debug("НАЧАЛО РАБОТА БОТА")
        await dp.start_polling(bot)
        yield
    finally:
        if redis_provider:
            await redis_provider.close()


async def main():
    async with init_all():
        pass


if __name__ == "__main__":
    asyncio.run(main())
