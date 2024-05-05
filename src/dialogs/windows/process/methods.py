from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogProtocol

from src.api.api import get_all_voices


async def getter_choice(dialog_manager: DialogManager, **kwargs):
    all_voices = []
    for key, name in get_all_voices().items():
        all_voices.append([key, name])
    return {"voices": all_voices}


async def start_send_win(message: Message, dialog: DialogProtocol, manager: DialogManager, voice_id: int):
    manager.dialog_data["voice_id"] = voice_id
    await manager.next()
