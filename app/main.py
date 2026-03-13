# Основной файл приложения
# Источник https://habr.com/ru/companies/amvera/articles/826196/
#
# Установить библиотеки (зависимости)
# pip install -r requirements.txt

from fastapi import FastAPI
import os
from typing import Optional
from utils import json_to_dict_list

# Получаем путь к директории (/app), где лежит текущий скрипт (main.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Получаем путь к JSON
path_to_json = os.path.join(script_dir, 'models/students.json')

# Сокращаем запись
# path_to_json = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'students.json')

app = FastAPI()
@app.get("/students")
def get_all_students(course: Optional[int] = None, major: Optional[str] = None):
    students = json_to_dict_list(path_to_json)
    return_list = []
    if course:
        for student in students:
            if student["course"] == course:
                return_list.append(student)
        # return return_list

    if major:
        return_list = [ student
            for student in return_list
                if student["major"] == major
        ]


    # if major:
    #     return_list = [student for student in return_list if student['major'].lower() == major.lower()]

    return return_list

@app.get("/students/{course}")
def get_all_students_course(course: int):
    students = json_to_dict_list(path_to_json)
    return_list = []
    for student in students:
        if student["course"] == course:
            return_list.append(student)
    return return_list

@app.get("/")
def home_page():
    return {"message": "Hello, world!"}