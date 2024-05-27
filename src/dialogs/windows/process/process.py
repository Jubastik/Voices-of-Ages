import operator
from operator import itemgetter

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Multiselect, Back, Radio
from aiogram_dialog.widgets.text import Const, Format

from src.dialogs.states import ProcessSG
from src.dialogs.windows.process.methods import getter_choice, start_send_win, handle_audio, getter_convert, octaves, \
    set_octave, stop_updater

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
    Const("Запишите голосовое сообщение\nМожете изменить высоту голоса:"),
    Radio(
        Format("> {item[0]}"),
        Format("{item[0]}"),
        id="r_octaves",
        item_id_getter=operator.itemgetter(1),
        on_state_changed=set_octave,
        items=octaves,
    ),
    Back(Const("Назад")),
    MessageInput(handle_audio),
    state=ProcessSG.send,
)

ConvertProcessWin = Window(
    Format("Ожидайте\n{status}"),
    Back(Const("Отмена"), on_click=stop_updater),
    getter=getter_convert,
    state=ProcessSG.convert,
)
