import asyncio
import logging
import os

from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram_dialog import DialogManager, DialogProtocol, ShowMode
from aiogram_dialog.manager.bg_manager import BgManager
from aiogram_dialog.widgets.kbd import ManagedRadio
from gradio_client.client import Job

from src.api.api import get_all_voices, start_convert, load_audio
from src.dialogs.states import ProcessSG

octaves = (
    ("-12", -12),
    ("-8", -8),
    ("-4", -4),
    ("0", 0),
    ("4", 4),
    ("8", 8),
    ("12", 12),
)

stop_users = set()


async def getter_choice(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["status_code"] = "Начало"
    all_voices = []
    for key, name in get_all_voices().items():
        all_voices.append([name, name])
    return {"voices": all_voices}


async def getter_convert(dialog_manager: DialogManager, **kwargs):
    status = f"Текущий статус: {dialog_manager.dialog_data.get('status_code')}"
    if dialog_manager.dialog_data.get("status_queue_size"):
        status += f"\nМесто в очереди: {dialog_manager.dialog_data.get('status_queue_size')}"
    return {"status": status}


async def start_send_win(message: Message, dialog: DialogProtocol, manager: DialogManager, voice):
    manager.dialog_data["voice_name"] = voice

    await manager.next()


async def set_octave(message: CallbackQuery, radio: ManagedRadio, manager: DialogManager, octave: int):
    manager.dialog_data["octave"] = octave


async def handle_audio(message: Message, dialog: DialogProtocol, manager: DialogManager):
    if message.voice is None:
        return
    if message.voice.duration > 60 * 4:
        await message.answer("Максимальная длительность аудио 4 минуты")
        return

    asyncio.create_task(
        start_ml(message, manager.dialog_data["voice_name"], int(manager.dialog_data.get("octave", 0)), manager.bg())
    )
    await manager.next()


async def start_ml(message: Message, voice_name, octave, manager: BgManager):
    from src.__main__ import bot

    if message.from_user.id in stop_users:
        stop_users.remove(message.from_user.id)

    file_path = await bot.get_file(message.voice.file_id)
    # Загружаем файл
    voice_file = await bot.download_file(file_path.file_path)

    # Сохраняем файл на диск
    with open(f'inp_audio/{message.message_id}.oga', 'wb') as f:
        f.write(voice_file.read())

    local_url = await load_audio(f"inp_audio/{message.message_id}.oga")
    os.remove(f'inp_audio/{message.message_id}.oga')

    job = await start_convert(voice_name, local_url, octave)
    await status_updater(voice_name, job, manager)


async def stop_updater(message: Message, dialog: DialogProtocol, manager: DialogManager):
    stop_users.add(message.from_user.id)


async def status_updater(voice_name: str, job: Job, manager: BgManager):
    from src.__main__ import bot

    while job.status().success is None:
        await asyncio.sleep(2)
        if manager.user.id in stop_users:
            stop_users.remove(manager.user.id)
            job.cancel()
            logging.info("Job canceled")
            return
        await manager.update(
            {"status_code": job.status().code.name, "status_queue_size": job.status().queue_size})

    if job.status().success:
        audio_path = job.result()[1]
        audio = FSInputFile(audio_path)
        await bot.send_audio(chat_id=manager.user.id, audio=audio, title=f"Результат {voice_name}")
    await asyncio.sleep(2)
    await manager.switch_to(ProcessSG.send, show_mode=ShowMode.DELETE_AND_SEND)
