import json

with open("src/db/models.json", "r") as f:
    models: dict = json.load(f)


def get_all_voices():
    return [(i, models[i]["title"]) for i in models.keys()]  # (id, title)


def get_model_url(model_id):
    return models[model_id]["pth"]


def get_index_url(model_id):
    return models[model_id]["index"]


def get_tts_voice(model_id):
    return models[model_id]["tts"]
