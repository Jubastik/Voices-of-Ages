from aiogram import Dispatcher

from src.dialogs.dialogs import MenuDLG, ProcessDLG


def register_dialogs(dp: Dispatcher):
    dp.include_router(MenuDLG)
    dp.include_router(ProcessDLG)
