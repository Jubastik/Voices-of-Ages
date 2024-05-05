from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const, Format

from src.dialogs.states import MenuSG, ProcessSG
from src.dialogs.windows.menu.methods import getter_menu

MainMenuWin = Window(
    Format("Привет {name} {sticker}"),
    Start(Const("Озвучить цитату"), state=ProcessSG.choice, id="choice_btn"),
    getter=getter_menu,
    state=MenuSG.main,
)
