from aiogram import F, Router
from aiogram.types import CallbackQuery

from adapters.uow import UnitOfWork
from callback_factory import (
    Action,
    ActionCallback,
    Page,
    PaginateCallback,
    CatalogItemCallback
)
from dto import Catalog
from domain import Service, Category
from keyboards import  get_catalog_kb, get_service_kb
from lexicon import catalog as lexicon


router = Router(name="catalog")

PAGE_LIMIT = 5



async def render_catalog(
    callback: CallbackQuery,
    uow: UnitOfWork,
    *,
    page: Page,
    offset: int = 0,
    limit: int = PAGE_LIMIT,
    category_id: int | None = None
):
    async with uow:
        if page == Page.SERVICE:
            catalog: Catalog[Service] = await uow.catalog.get_services(
                category_id=category_id,
                offset=offset,
                limit=limit,
            )
            if category_id is None:
                text = lexicon.SERVICES
            else:
                category = await uow.generic.read_one(
                    Category,
                    id=category_id,
                    with_raise=True,
                )
                text = lexicon.category_services(category.name)

        else:
            catalog: Catalog[Category] = await uow.catalog.get_categories(
                offset=offset,
                limit=limit,
            )
            text = lexicon.CATEGORIES

    await callback.message.edit_text(
        text=text,
        reply_markup=get_catalog_kb(
            page=page,
            items = catalog.content,
            offset=offset,
            limit=limit,
            total=catalog.total,
            category_id=category_id
        ),
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
        page=Page.SERVICE
    )


@router.callback_query(
    PaginateCallback.filter(
        F.page == Page.SERVICE
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
        page=callback_data.page,
        category_id=callback_data.category_id
    )

@router.callback_query(
    CatalogItemCallback.filter(
        F.page == Page.SERVICE
    )
)
async def process_service(
    callback: CallbackQuery,
    callback_data: CatalogItemCallback,
    uow: UnitOfWork,
):
    async with uow:
        service = await uow.generic.read_one(
            Service,
            id=callback_data.id,
            with_raise=True,
        )
    keyboard = get_service_kb(
        offset=callback_data.offset,
        limit=callback_data.limit,
        category_id=callback_data.category_id,
    )
    await callback.message.edit_text(
        text=lexicon.service_card(service),
        reply_markup=keyboard,
    )


@router.callback_query(
    CatalogItemCallback.filter(
        F.page == Page.CATEGORY
    )
)
async def process_category(
    callback: CallbackQuery,
    callback_data: CatalogItemCallback,
    uow: UnitOfWork,
):
    # async with uow:
    #     category = await uow.generic.read_one(
    #         Category,
    #         id=callback_data.id,
    #         with_raise=True,
    #     )

    await render_catalog(
        callback=callback,
        uow=uow,
        page=Page.SERVICE,
        category_id=callback_data.id,
        offset=0,
        limit=callback_data.limit,
    )