from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

import domain
from adapters.uow import UnitOfWork
from callback_factory import Action, ActionCallback
from keyboards import get_inline_kb
from lexicon import core
from domain import AlreadyExistsError
from usecases.user import create_user, create_seller


router = Router(name="command_core")

async def get_menu_appropriate_user(uow, received_obj: Message | CallbackQuery):
    try:
        async with uow:
            await uow.db.read_one(
                uow,
                telegram_id=received_obj.from_user.id,
                with_raise=True
            )
    except AlreadyExistsError:
        body = dict(text=core.START, reply_markup=get_registration_menu())
        if isinstance(received_obj, Message):
            await received_obj.answer(**body)
        else:
            await received_obj.message.edit_text(**body)
        return



def get_main_menu():
    return get_inline_kb(
        Action.CATALOG,
        Action.SEARCH,
        Action.FAVORITES,
        Action.ORDERS,
        width=2,
    )


def get_registration_menu():
    return get_inline_kb(
        Action.REGISTER_USER,
        Action.REGISTER_SELLER,
        width=1,
    )


@router.message(CommandStart())
async def process_command_start(
    message: Message,
    uow: UnitOfWork,
):
    await get_menu_appropriate_user(uow=uow, received_obj=message)

    await message.answer(
        text=core.WELCOME_BACK,
        reply_markup=get_main_menu(),
    )


@router.message(Command("help"))
async def process_command_help(message: Message):
    await message.answer(
        text=core.HELP,
        reply_markup=get_inline_kb(Action.MENU),
    )


@router.callback_query(
    ActionCallback.filter(
        F.action == Action.REGISTER_USER
    )
)
async def process_register_user(
    callback: CallbackQuery,
    uow: UnitOfWork,
):
    user = domain.User(
        id=callback.from_user.id,
        username=callback.from_user.username,
    )
    await create_user(uow=uow,user=user)

    await callback.message.edit_text(
        text=core.WELCOME_BACK,
        reply_markup=get_main_menu(),
    )


@router.callback_query(
    ActionCallback.filter(
        F.action == Action.REGISTER_SELLER
    )
)
async def process_register_seller(
    callback: CallbackQuery,
    uow: UnitOfWork,
):
    seller = domain.Seller(
        id=callback.from_user.id,
        username=callback.from_user.username,
    )

    await create_seller(
        uow=uow,
        seller=seller,
    )

    await callback.message.edit_text(
        text=core.WELCOME_BACK,
        reply_markup=get_main_menu(),
    )


@router.callback_query(
    ActionCallback.filter(
        F.action == Action.MENU
    )
)
async def process_menu(
    callback: CallbackQuery,
    uow: UnitOfWork,
):
    await get_menu_appropriate_user(uow=uow, received_obj=callback)

    await callback.message.edit_text(
        text=core.WELCOME_BACK,
        reply_markup=get_main_menu(),
    )


@router.callback_query(
    ActionCallback.filter(
        F.action == Action.HELP
    )
)
async def process_help(callback: CallbackQuery):
    await callback.message.edit_text(
        text=core.HELP,
        reply_markup=get_inline_kb(Action.MENU),
    )