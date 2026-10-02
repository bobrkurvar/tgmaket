from aiogram.filters.callback_data import CallbackData
from enum import StrEnum


class Action(StrEnum):
    MENU = "menu"
    HELP = "help"
    REGISTER_USER = "register_user"
    REGISTER_SELLER = "register_seller"
    CATALOG = "catalog"
    SEARCH = "search"
    FAVORITES = "favorites"
    ORDERS = "orders"


class ActionCallback(CallbackData, prefix="action"):
    action: Action


class Page(StrEnum):
    CATALOG = "catalog"
    CATEGORY = "category"
    FAVORITES = "favorites"


class PaginateCallback(CallbackData, prefix="page"):
    page: Page
    offset: int
    limit: int