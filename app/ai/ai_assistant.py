import requests
import urllib3
import json
import os

def ai_model_list():
    from openai import OpenAI
    client = OpenAI(
        base_url="https://alfagen.moscow.alfaintra.net/continue-dev",
        api_key="04e8a51a-b5d8-4c55-ba3a-05632cde66b8",
    )
    return client.models.list()

# для подключения к ИИ
def ai_connect(promt):

    # Читаем конфиг ИИ-ассистента
    try:
        # Получаем путь к директории (/app), где лежит текущий скрипт (main.py)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Получаем путь к JSON со студентами
        path_to_json_config = os.path.join(script_dir, 'config.json')
        with open(path_to_json_config, 'r', encoding='utf-8') as file:
            json_str = file.read()
            # print(json_str)
            ai_config = json.loads(json_str)
        # return ai_config
    except (TypeError, ValueError, IOError) as e:
        print(f"Ошибка при чтении JSON из файла или преобразовании в список словарей: {e}")

    # Определяем константы
    AI_URL = ai_config["base_url"]
    AI_KEY = ai_config["api_key"]
    AI_MODEL = ai_config["model"]

    # Определяем параметры запроса к ИИ
    url = AI_URL
    headers = {
        "Authorization": "Bearer " + AI_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "model": AI_MODEL,
        "messages": [{"role": "user", "content": promt}],
        "stream": False,
    }

    resp = requests.post(url, headers=headers, json=payload, verify=False)

    return (json.loads(resp.text)["choices"][0]["message"]["content"])