import asyncio

from aiogram.types import Message, FSInputFile
from aiogram_dialog import DialogManager, DialogProtocol, ShowMode
from aiogram_dialog.manager.bg_manager import BgManager
from gradio_client.client import Job

from src.api.api import get_all_voices, start_convert
from src.settings import settings


async def getter_choice(dialog_manager: DialogManager, **kwargs):
    all_voices = []
    for key, name in (await get_all_voices()).items():
        all_voices.append([name, name])
    return {"voices": all_voices}


async def getter_convert(dialog_manager: DialogManager, **kwargs):
    return {"status": dialog_manager.dialog_data.get("status", "Начало")}


async def start_send_win(message: Message, dialog: DialogProtocol, manager: DialogManager, voice):
    manager.dialog_data["voice_name"] = voice

    await manager.next()


async def handle_audio(message: Message, dialog: DialogProtocol, manager: DialogManager):
    from src.__main__ import bot
    if message.voice is None:
        return
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    download_url = f'https://api.telegram.org/file/bot{settings.token.get_secret_value()}/{file_path}'
    job = await start_convert(manager.dialog_data["voice_name"], download_url)
    asyncio.create_task(status_updater(job, manager.bg()))

    await manager.next()


async def status_updater(job: Job, manager: BgManager):
    from src.__main__ import bot

    while job.status().success is None:
        await asyncio.sleep(1)
        await manager.update({"status": str(job.status().code.name)})
    if job.status().success:
        audio_path = job.result()[1]
        audio = FSInputFile(audio_path)
        await bot.send_audio(chat_id=manager.user.id, audio=audio, title="Результат")
    await asyncio.sleep(1)
    await manager.done(show_mode=ShowMode.DELETE_AND_SEND)
