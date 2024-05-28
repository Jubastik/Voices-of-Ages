import asyncio
import logging

from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram_dialog import DialogManager, DialogProtocol, ShowMode
from aiogram_dialog.manager.bg_manager import BgManager
from aiogram_dialog.widgets.kbd import ManagedRadio
from gradio_client.client import Job

from src.api.api import start_convert
from src.db.fake_database import get_all_voices, get_model_url, get_index_url
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
    return {"voices": get_all_voices()}


async def getter_convert(dialog_manager: DialogManager, **kwargs):
    status = f"Текущий статус: {dialog_manager.dialog_data.get('status_code')}"
    if dialog_manager.dialog_data.get("status_queue_size"):
        status += f"\nМесто в очереди: {dialog_manager.dialog_data.get('status_queue_size')}"
    return {"status": status}


async def start_send_win(message: Message, dialog: DialogProtocol, manager: DialogManager, voice):
    manager.dialog_data["voice_id"] = voice
    await manager.next()


async def set_octave(message: CallbackQuery, radio: ManagedRadio, manager: DialogManager, octave: int):
    manager.dialog_data["octave"] = octave


async def handle_audio(message: Message, dialog: DialogProtocol, manager: DialogManager):
    manager.dialog_data["status_code"] = "Начало"
    if message.voice is None:
        return
    if message.voice.duration > 60 * 4:
        await message.answer("Максимальная длительность аудио 4 минуты")
        return

    asyncio.create_task(
        start_ml(message, manager.dialog_data["voice_id"], int(manager.dialog_data.get("octave", 0)), manager.bg())
    )
    await manager.next()


async def start_ml(message: Message, voice_id, octave, manager: BgManager):
    from src.__main__ import bot

    if message.from_user.id in stop_users:
        stop_users.remove(message.from_user.id)

    file_path = await bot.get_file(message.voice.file_id)
    # Загружаем файл
    voice_file = await bot.download_file(file_path.file_path)

    audio_url = f'inp_audio/{message.message_id}.oga'
    # Сохраняем файл на диск
    with open(audio_url, 'wb') as f:
        f.write(voice_file.read())

    model_url = get_model_url(voice_id)
    index_url = get_index_url(voice_id)

    job = await start_convert(audio_url, model_url, index_url, octave)
    await status_updater(voice_id, job, manager)


async def stop_updater(message: Message, dialog: DialogProtocol, manager: DialogManager):
    stop_users.add(message.from_user.id)


async def status_updater(voice_id: str, job: Job, manager: BgManager):
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
        audio_path = job.result()[0]
        audio = FSInputFile(audio_path)
        await bot.send_audio(chat_id=manager.user.id, audio=audio, title=f"Результат {voice_id}")
    await asyncio.sleep(2)
    await manager.switch_to(ProcessSG.send, show_mode=ShowMode.DELETE_AND_SEND)
