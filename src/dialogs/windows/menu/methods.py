from random import choice

from aiogram_dialog import DialogManager

stickers = ['👍', '👻', '😄', '🧐', '👀', '🌝', '🎫', '🔫', '📌', '📚']


async def getter_menu(dialog_manager: DialogManager, **kwargs):
    name = kwargs["event_from_user"].first_name
    return {"name": name,
            "sticker": choice(stickers),
            }
