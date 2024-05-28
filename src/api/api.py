import gradio_client
from gradio_client import Client
from gradio_client.client import Job

from src.settings import settings

ml_client = Client(settings.gradio_url, output_dir="./out_audio")


async def start_convert(audio_url, model_url, index_url, octave) -> Job:
    data = [
        [gradio_client.file(audio_url)],
        gradio_client.file(model_url), "rmvpe+",
        octave,
        gradio_client.file(index_url), 0, 3,
        0.25, 0.5, False,
        False
    ]
    print(data)
    job = ml_client.submit(*data, api_name="/run")
    return job
