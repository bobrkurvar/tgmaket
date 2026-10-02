from aiogram import Router
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from middleware import DeleteUsersMessage

from . import command_core

main_router = Router()
main_router.include_routers(command_core.router)
main_router.callback_query.outer_middleware(CallbackAnswerMiddleware())
main_router.message.outer_middleware(DeleteUsersMessage())
