import requests
import urllib3
import json
import os
from openai import OpenAI
from typing import List, Dict, Optional, Callable

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
AI_URL_REQUEST = ai_config["base_url_request"]
AI_URL = ai_config["base_url"]
AI_KEY = ai_config["api_key"]
AI_MODEL = ai_config["model"]

client = OpenAI(
    base_url=AI_URL,
    api_key=AI_KEY,
)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Возвращает текущую дату и время в формате ISO.",
            "parameters": {}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_products",
            "description": "Возвращает перечень или список товаров из магазина",
            "parameters": {}
        }
    },
]
def ai_model_list():
    return client.models.list()

# для подключения к ИИ через Request
def ai_connect_request(messages):
    # Определяем параметры запроса к ИИ
    url = AI_URL_REQUEST
    headers = {
        "Authorization": "Bearer " + AI_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "model": AI_MODEL,
        "messages": messages,
        "tools": tools,
        "stream": False,
    }
    # Реализация через стандартный request
    response = requests.post(url, headers=headers, json=payload, verify=False)
    return (json.loads(response.text)["choices"][0]["message"]["content"])

# для подключения к ИИ через OpenAi
def ai_connect(messages):
    # messages = [{"role": "user", "content": "Какая текущая дата?"}]   # пробный промт
    response = client.chat.completions.create(
        model=AI_MODEL,
        messages=messages,
        tools=tools,
        stream=False
    )
    return response.choices[0].message.model_dump()

    # Пример ответа model_dump()
    #
    # {"models":{"content":"","refusal":null,"role":"assistant","annotations":null,"audio":null,"function_call":null,
    # "tool_calls":[
    # {"id":"call_3e7225b132974a038075c2f1",
    #   "function":{
    #       "arguments":"{}",
    #       "name":"get_current_time"
    #   },
    # "type":"function",
    # "index":0}
    # ],"reasoning_content":"The user asks for the current date. I'll use the get_current_time tool."}}


def ai_agent(promt):
    # Определяем промт
    messages = [{"role": "user", "content": promt}]
    print(promt)
    while True:  # цикл инструментов
        # Обращение к модели
        model_response = ai_connect(messages)
        if model_response.get("tool_calls"):
            for tc in model_response["tool_calls"]:
                tool_name = tc["function"]["name"]
                tool_args = tc["function"]["arguments"]
                result = execute_tool(tool_name)    # todo: добавить аргумент "tool_args"
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": str(result)
                })
                print(result)
        else:
            assistant_msg = model_response["content"]
            break
    return assistant_msg

#
# Использовать инструмент
#
# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_current_time",
#             "description": "Возвращает текущую дату и время в формате ISO.",
#             "parameters": {}
#         }
#     }
# ]


def execute_tool(tool_name: str) -> str:    # todo: Добавить агрумент "tool_args: dict"
    if tool_name == "get_current_time":
        from datetime import datetime
        return datetime.now().isoformat()+" и счастье!"
    if tool_name == "get_products":
        from app.main import get_all_products
        return get_all_products()
    return f"Инструмент {tool_name} не найден."
