import logging

from aiogram import Router
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent

dlg_router = Router()


@dlg_router.message(CommandStart())
async def handle_start_query(message: Message, dialog_manager: DialogManager):
    await message.answer("Ура")


#     await starting_dispatcher(message, dialog_manager)
#
#
# async def starting_dispatcher(message: Message, dialog_manager: DialogManager):
#     await dialog_manager.start(MenuSG.main, mode=StartMode.RESET_STACK)


async def error_handler(event, dialog_manager: DialogManager):
    logging.error(event.exception)
    if isinstance(event.exception, UnknownIntent):
        # Handling an error related to an outdated callback
        await handle_start_query(event.update.callback_query, dialog_manager)
    else:
        return UNHANDLED
