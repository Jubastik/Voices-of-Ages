from gradio_client import Client
from gradio_client.client import Job

from src.settings import settings

ml_client = Client(settings.gradio_url, upload_files=False)


async def get_all_voices():
    gradio_query = ml_client.predict(api_name="/infer_refresh")

    names = {ind: name[0].replace(".pth", "") for ind, name in enumerate(gradio_query[0]["choices"])}
    return names


async def start_convert(voice_name, audio_url) -> Job:
    data = [
        0,
        audio_url,
        0,
        None,
        "rmvpe",
        "",
        "",
        0.75,
        3,
        0,
        0.25,
        0.33
    ]
    ml_client.predict(f"{voice_name}.pth", 0.33, 0.33, api_name="/infer_set")
    job = ml_client.submit(*data, api_name="/infer_convert")
    return job


async def check_convert_status(job: Job):
    return job.status()
