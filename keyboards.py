import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback_factory import Action, ActionCallback, PaginateCallback, Page

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

def get_inline_kb(
    *actions: Action,
    width: int = 1,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for action in actions:
        builder.button(
            text=ACTION_TEXT[action],
            callback_data=ActionCallback(
                action=action,
            ).pack(),
        )

    builder.adjust(width)

    return builder.as_markup()


def get_pagination_kb(
    *,
    page: Page,
    offset: int,
    limit: int,
    total: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if offset > 0:
        builder.button(
            text="←",
            callback_data=PaginateCallback(
                offset=max(0, offset - limit),
                limit=limit,
                page=page
            ).pack(),
        )

    if offset + limit < total:
        builder.button(
            text="→",
            callback_data=PaginateCallback(
                offset=offset + limit,
                limit=limit,
                page=page
            ).pack(),
        )

    builder.adjust(2)

    return builder.as_markup()