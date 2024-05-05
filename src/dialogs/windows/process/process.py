from operator import itemgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Multiselect, Back
from aiogram_dialog.widgets.text import Const, Format

from src.dialogs.states import ProcessSG
from src.dialogs.windows.process.methods import getter_choice, start_send_win

ChoiceProcessWin = Window(
    Const("Выберите голос"),
    ScrollingGroup(
        Multiselect(
            Format("{item[1]}"),
            Format("{item[1]}"),
            id="ms",
            items="voices",
            item_id_getter=itemgetter(0),
            on_click=start_send_win
        ),
        width=1,
        height=5,
        id="choice_voice_btn",
    ),
    Cancel(Const("Меню")),
    getter=getter_choice,
    state=ProcessSG.choice,
)

SendProcessWin = Window(
    Const("Запишите голосовое сообщение:"),
    Back(Const("Назад")),
    state=ProcessSG.send,
)
