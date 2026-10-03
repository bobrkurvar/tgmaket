from aiogram import F, Router
from aiogram.types import CallbackQuery

from adapters.uow import UnitOfWork
from callback_factory import (
    Action,
    ActionCallback,
    Page,
    PaginateCallback,
)
from keyboards import get_pagination_kb
from usecases.catalog import get_catalog_data
from lexicon import catalog as lexicon


router = Router(name="catalog")

PAGE_LIMIT = 5


async def render_catalog(
    callback: CallbackQuery,
    uow: UnitOfWork,
    *,
    offset: int = 0,
    limit: int = PAGE_LIMIT,
):
    categories, total = await get_catalog_data(
        uow=uow,
        limit=limit,
        offset=offset
    )

    text = lexicon.CATALOG

    pagination = get_pagination_kb(
        page=Page.CATALOG,
        offset=offset,
        limit=limit,
        total=total,
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=pagination,
    )


@router.callback_query(
    ActionCallback.filter(
        F.action == Action.CATALOG
    )
)
async def process_catalog(
    callback: CallbackQuery,
    uow: UnitOfWork,
):
    await render_catalog(
        callback=callback,
        uow=uow,
    )


@router.callback_query(
    PaginateCallback.filter(
        F.page == Page.CATALOG
    )
)
async def process_catalog_pagination(
    callback: CallbackQuery,
    callback_data: PaginateCallback,
    uow: UnitOfWork,
):
    await render_catalog(
        callback=callback,
        uow=uow,
        offset=callback_data.offset,
        limit=callback_data.limit,
    )