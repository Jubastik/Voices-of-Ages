import logging

from aiogram import Router
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from httpx import ConnectError

from src.dialogs.states import MenuSG

dlg_router = Router()


@dlg_router.message(CommandStart())
async def handle_start_query(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MenuSG.main)


async def error_handler(event, dialog_manager: DialogManager):
    logging.error(event.exception)
    if isinstance(event.exception, UnknownIntent):
        # Handling an error related to an outdated callback
        await handle_start_query(event.update.callback_query, dialog_manager)
    elif isinstance(event.exception, UnknownState):
        await handle_start_query(event.update.callback_query, dialog_manager)
    elif isinstance(event.exception, ConnectError):
        await event.update.callback_query.answer("ML сервис запускается. Повторите попытку через 30 секунд", show_alert=True)
    else:
        return UNHANDLED
