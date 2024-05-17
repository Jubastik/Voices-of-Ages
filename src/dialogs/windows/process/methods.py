import asyncio
import os
from io import BytesIO

from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram_dialog import DialogManager, DialogProtocol, ShowMode
from aiogram_dialog.manager.bg_manager import BgManager
from aiogram_dialog.widgets.kbd import ManagedRadio
from gradio_client.client import Job
from pydub import AudioSegment

from src.api.api import get_all_voices, start_convert, load_audio

octaves = (
    ("⬇️", -12),
    ("↘️", -6),
    ("0️⃣", 0),
    ("↗️", 6),
    ("⬆️", 12),
)


async def getter_choice(dialog_manager: DialogManager, **kwargs):
    all_voices = []
    for key, name in get_all_voices().items():
        all_voices.append([name, name])
    return {"voices": all_voices}


async def getter_convert(dialog_manager: DialogManager, **kwargs):
    status = f"Текущий статус: {dialog_manager.dialog_data.get('status_code', 'Начало')}"
    if dialog_manager.dialog_data.get("status_queue_size"):
        status += f"\nМесто в очереди: {dialog_manager.dialog_data.get('status_queue_size')}"
    return {"status": status}


async def start_send_win(message: Message, dialog: DialogProtocol, manager: DialogManager, voice):
    manager.dialog_data["voice_name"] = voice

    await manager.next()


async def set_octave(message: CallbackQuery, radio: ManagedRadio, manager: DialogManager, octave: int):
    manager.dialog_data["octave"] = octave


async def handle_audio(message: Message, dialog: DialogProtocol, manager: DialogManager):
    from src.__main__ import bot
    if message.voice is None:
        return
    await manager.next()

    file_path = await bot.get_file(message.voice.file_id)
    # Загружаем файл
    voice_file = await bot.download_file(file_path.file_path)

    # Конвертируем OGG в MP3
    audio = AudioSegment.from_ogg(voice_file)
    mp3_bytes = BytesIO()
    audio.export(mp3_bytes, format='mp3')
    mp3_bytes.seek(0)  # Сбрасываем указатель в начало

    # Сохраняем файл на диск
    with open(f'inp_audio/{message.message_id}.mp3', 'wb') as f:
        f.write(mp3_bytes.read())

    local_url = await load_audio(f'inp_audio/{message.message_id}.mp3')
    os.remove(f'inp_audio/{message.message_id}.mp3')

    job = await start_convert(manager.dialog_data["voice_name"], local_url, int(manager.dialog_data.get("octave", 0)))
    asyncio.create_task(status_updater(job, manager.bg()))


async def status_updater(job: Job, manager: BgManager):
    from src.__main__ import bot

    while job.status().success is None:
        await asyncio.sleep(1)
        await manager.update(
            {"status_code": job.status().code.name, "status_queue_size": job.status().queue_size})
    if job.status().success:
        audio_path = job.result()[1]
        audio = FSInputFile(audio_path)
        await bot.send_audio(chat_id=manager.user.id, audio=audio, title="Результат")
    await asyncio.sleep(1)
    await manager.done(show_mode=ShowMode.DELETE_AND_SEND)
