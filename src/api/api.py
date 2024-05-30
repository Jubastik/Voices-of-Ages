import asyncio

import gradio_client
from gradio_client import Client
from gradio_client.client import Job

from src.settings import settings

ml_client = Client(settings.gradio_url, output_dir="./out_audio")

status_translations = {
    "STARTING": "НАЧАЛО",
    "JOINING_QUEUE": "ПОДКЛЮЧЕНИЕ К ОЧЕРЕДИ",
    "QUEUE_FULL": "ОЧЕРЕДЬ ПОЛНА",
    "IN_QUEUE": "В ОЧЕРЕДИ",
    "SENDING_DATA": "ОТПРАВКА ДАННЫХ",
    "PROCESSING": "ОБРАБОТКА",
    "ITERATING": "ИТЕРАЦИЯ",
    "PROGRESS": "ПРОГРЕСС",
    "FINISHED": "ЗАВЕРШЕНО",
    "CANCELLED": "ОТМЕНЕНО",
    "LOG": "ОБРАБОТКА"
}

async def start_convert(audio_url, model_url, index_url, octave) -> Job:
    data = [
        [gradio_client.file(audio_url)],
        gradio_client.file(model_url), "rmvpe+",
        octave,
        gradio_client.file(index_url), 0, 3,
        0.25, 0.5, False,
        False
    ]
    job = ml_client.submit(*data, api_name="/run")
    return job


async def get_tts(text, voice):
    audio_path = ml_client.submit(
        tts_voice=voice,
        tts_text=text,
        play_tts=False,
        api_name="/infer_tts_audio"
    )
    while audio_path.status().success is None:
        await asyncio.sleep(2)

    return audio_path.result()[0][0]
