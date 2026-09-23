# Основной файл приложения
# Источник https://habr.com/ru/companies/amvera/articles/826196/
#
# Установить библиотеки (зависимости)
# pip install -r requirements.txt
#
# 1) Запустить сервер
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# или для HTTPS
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --ssl-keyfile "./cert/device.key" --ssl-certfile "./cert/localhost.crt"
# 2) Запустить Postrge SQL
# pg_ctl -D /usr/local/var/postgres start
# ИЛИ остановить:
# pg_ctl -D /usr/local/var/postgres stop
# Swagger
# http://192.168.68.105:8000/docs#/default/get_all_students_course_students__course__get
#
# Ресурс будет доступен по адресам:
# http://192.168.68.106:8000/ (нужно предварительно выяснить IP-адрес ПК в локальной сети, например, ifconfig | grep "inet" | grep "broadcast")
# http://localhost:8000/
# Выпуск rootCA сертификата для HTTPS
# openssl req -newkey rsa:1024 -x509 -sha256 -days 365 -out certificate.cert -keyout certificate.key -nodes -subj "/C=RUS/ST=RO/L=Rostov-on-Don/O=MySelf/OU=MySelfUnit/CN=macbook/emailAddress=demyanchenko.ao@gmail.com"
# openssl req -new -newkey rsa:2048 -sha256 -nodes -keyout device.key -subj "/C=CA/ST=None/L=NB/O=None/CN=Product Server" -out device.csr


# Добавляем внутренний каталог для импорта
import sys

sys.path.append('./app')
sys.path.append('./app/models')
sys.path.append('./app/api')
sys.path.append('./app/ai')
from fastapi import FastAPI, Body, status, Query
from fastapi.responses import JSONResponse
import os
from typing import Optional
from file_utils import json_to_dict_list

# Получаем путь к директории (/app), где лежит текущий скрипт (main.py)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Получаем путь к JSON со студентами
path_to_json_students = os.path.join(script_dir, 'models/students.json')
# Получаем путь к JSON с продуктами
path_to_json_products = os.path.join(script_dir, 'models/products.json')
# Сокращаем запись
# path_to_json = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'students.json')


import product

# условная база данных - набор объектов Product
# products = [Product("Nike shoes", 10.5, 1), Product("Adidas shoes", 13.0, 20)]
# products = json_to_dict_list(path_to_json_products)

# Подключаем БД
from db_manager import connect, db_execute_query, db_select_product_by_id, db_input_product, db_update_product_by_id, db_delete_product_by_id
connection = connect()

app = FastAPI()

# Корневой API
#
@app.get("/")
def home_page():
    # print(ai_model_list())
    return {"message": "Hello, world!"}


# Заголовок ресурса
#
@app.head("/products")
def head_source():
    return {"message": "HEAD response"}

# API продукта
#/Users/demyanchenkoao/API/app/resp.txt
@app.get("/products")
def get_all_products():
    query = "SELECT * FROM product;"
    result = db_execute_query(connection, query)
    products = []
    for product in result:
        product = {
            "id": product[0],
            "title": product[1],
            "price": product[2],
            "quantity": product[3]
        }
        products.append(product)
    return products

@app.post("/product")
async def create_product(data = Body()):
    product = Product(data["title"], data["price"], data["quantity"])
    # добавляем объект в список products
    products.append(product)
    return product
    return {"message": "POST запрос выполнен успешно", "data": data}

@app.put("/product")
async def put_product(data  = Body()):
    # print("data--: ",data)
    # получаем пользователя по id (если указан)
    if 'id' in data:
        print("finded 'id' in 'data'")
        # print(data["id"])
        product = db_select_product_by_id(connection, data["id"])
    else:
        # иначе направляем на создание нового ресурса
        print("Not found index 'id' in 'data'")
        product = None
    print("product--: ",product)
    # если ресурс не найден
    if product == None:
        # если не найден, добавляем новый продукт в список products
        product = db_input_product(connection, data["title"], data["price"], data["quantity"])
        product = {
            "id": product[0],
            "title": product[1],
            "price": product[2],
            "quantity": product[3]
        }
        print("Аdd product: ", product)
        return {"message": "PUT запрос выполнен успешно, создан новый продукт", "data": product}
    else:
        # если продукт найден, изменяем его данные и отправляем обратно клиенту
        product = db_update_product_by_id(connection, data["title"], data["price"], data["quantity"], data["id"])
        print("Update product: ", product)
    return {"message": "PUT запрос выполнен успешно, продукт изменён", "data": data}

@app.delete("/product/{id}")
def delete_product(id):
    product = db_select_product_by_id(connection, id)
    if product == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={ "message": "Продукт не найден" }
        )
    deleted_id = db_delete_product_by_id(connection, id)
    if deleted_id:
        product = {
            "id": product[0],
            "title": product[1],
            "price": product[2],
            "quantity": product[3]
        }
        print("Delete product: ", product)
        return product
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={ "message": "Ошибка при удалении продукта" }
        )

# API авторизация пользователя
@app.post("/auth")
async def authorization_user(data = Body()):
    print(data)
    # print(data["login"], data["password"])
    # return product
    return {"message": "POST запрос выполнен успешно", "data": data}

# API студенты
#
@app.get("/students")
def get_all_students(course: Optional[int] = None, major: Optional[str] = None):
    students = json_to_dict_list(path_to_json_students)
    if course:
        students = [ student
            for student in students
                if student["course"] == course
        ]

    if major:
        students = [ student
            for student in students
                if student["major"] == major
        ]
    # if major:
    #     return_list = [student for student in return_list if student['major'].lower() == major.lower()]

    return students

@app.get("/students/{course}")
def get_all_students_course(course: int):
    students = json_to_dict_list(path_to_json_students)
    return_list = []
    for student in students:
        if student["course"] == course:
            return_list.append(student)
    return return_list


