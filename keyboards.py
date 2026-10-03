import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from callback_factory import Action, ActionCallback, PaginateCallback, Page, CatalogItemCallback
from domain import Service, Category
from collections.abc import Collection

log = logging.getLogger(__name__)

from lexicon import buttons


ACTION_TEXT = {
    Action.CATALOG: buttons.CATALOG,
    Action.SEARCH: buttons.SEARCH,
    Action.FAVORITES: buttons.FAVORITES,
    Action.ORDERS: buttons.ORDERS,
    Action.REGISTER_USER: buttons.BECOME_USER,
    Action.REGISTER_SELLER: buttons.BECOME_SELLER,
}


def build_inline_kb(
    *buttons: tuple[str, CallbackData],
    width: int = 1,
):
    builder = InlineKeyboardBuilder()

    for text, callback_data in buttons:
        builder.button(
            text=text,
            callback_data=callback_data,
        )

    builder.adjust(width)

    return builder.as_markup()


def get_action_kb(
    *actions: Action,
    width: int = 1,
):
    return build_inline_kb(
        *(
            (
                ACTION_TEXT[action],
                ActionCallback(action=action),
            )
            for action in actions
        ),
        width=width,
    )



def get_catalog_kb(
    page: Page,
    items: Collection[Service] | Collection[Category],
    offset: int,
    limit: int,
    total: int,
    category_id: int | None = None
):


    builder = InlineKeyboardBuilder()
    if page == page.SERVICE:
        for item in items:
            builder.button(
                text=item.title,
                callback_data=CatalogItemCallback(
                    id=item.id,
                    page=page,
                    offset=offset,
                    limit=limit,
                    category_id=category_id,
                ),
            )

    elif page == Page.CATEGORY:
        for item in items:
            builder.button(
                text=item.name,
                callback_data=CatalogItemCallback(
                    id=item.id,
                    page=page,
                    offset=offset,
                    limit=limit,
                    category_id=category_id,
                ),
            )
    else:
        raise ValueError(f"Неизвестная страница каталога: {page}")

    builder.adjust(1)

    # пагинация
    pagination = []

    if offset > 0:
        pagination.append(
            InlineKeyboardButton(
                text="←",
                callback_data=PaginateCallback(
                    page=page,
                    offset=max(0, offset - limit),
                    limit=limit,
                    category_id=category_id,
                ).pack(),
            )
        )

    if offset + limit < total:
        pagination.append(
            InlineKeyboardButton(
                text="→",
                callback_data=PaginateCallback(
                    page=page,
                    offset=offset + limit,
                    limit=limit,
                    category_id=category_id,
                ).pack(),
            )
        )

    if pagination:
        builder.row(*pagination)

    return builder.as_markup()


def get_service_kb(
    *,
    offset: int,
    limit: int,
    category_id: int | None = None,
):
    return build_inline_kb(
        (
            buttons.BACK,
            PaginateCallback(
                page=Page.SERVICE,
                offset=offset,
                limit=limit,
                category_id=category_id,
            ),
        ),
        (
            buttons.MENU,
            ActionCallback(
                action=Action.MENU,
            ),
        ),
    )