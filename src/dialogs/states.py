from aiogram.fsm.state import StatesGroup, State


class MenuSG(StatesGroup):
    main = State()


class ProcessSG(StatesGroup):
    choice = State()
    send = State()
    convert = State()


class ArchiveSG(StatesGroup):
    choice = State()
    details = State()
