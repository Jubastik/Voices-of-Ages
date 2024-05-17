from cachetools.func import ttl_cache
from gradio_client import Client
from gradio_client.client import Job

from src.settings import settings


async def load_audio(mp3path):
    ml_client = Client(settings.gradio_url, verbose=False)

    audio_path = ml_client.predict(mp3path, fn_index=1)
    return audio_path


@ttl_cache(ttl=120)
def get_all_voices():
    ml_client = Client(settings.gradio_url, upload_files=False, verbose=False)

    gradio_query = ml_client.predict(fn_index=9)
    names = {ind: name.replace(".pth", "") for ind, name in enumerate(gradio_query[0]["choices"])}
    return names


async def start_convert(voice_name, audio_url, octave) -> Job:
    ml_client = Client(settings.gradio_url, upload_files=False, verbose=False, output_dir="./out_audio")

    predict_settings = (
        ("speaker_id", 0),
        ("аудиозапись", audio_url),
        ("высота", octave),
        ("f0_curve", None),
        ("алгоритм извлечения", "rmvpe"),
        (".index ищется автоматически", f"./logs/added_IVF253_Flat_nprobe_1_{voice_name}_v2.index"),
        ("соотношение_поисковых_функций", 0),
        ("если_3_применить_медианную_фильтрацию", 3),
        ("0_for_no_resampling", 0),
        ("чем_ближе_это_соотношение_к_1_тем_больше_используется_огибающая_выходного_сигнала", 0.5),
        ("защита_безголосых_согласных", 0.5),
        ("mangiocrepe_hop_length", 64)
    )
    data = [v for k, v in predict_settings]

    ml_client.predict(f"{voice_name}.pth", fn_index=0)
    job = ml_client.submit(*data, fn_index=16)
    return job


async def check_convert_status(job: Job):
    return job.status()
