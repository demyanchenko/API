# Основной файл приложения
# Источник https://habr.com/ru/companies/amvera/articles/826196/
#
# Установить библиотеки (зависимости)
# pip install -r requirements.txt
#
# Swagger
# http://192.168.68.105:8000/docs#/default/get_all_students_course_students__course__get

# Добавляем внутренний каталог для импорта
import sys
sys.path.append('./app')
sys.path.append('./app/models')
sys.path.append('./app/api')

import uuid
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse
import os
from typing import Optional
from utils import json_to_dict_list, dict_list_to_json
from typing import List
import copy

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
from database import connect, execute_read_query, execute_one_record, execute_input_query, execute_update_query
connection = connect()

app = FastAPI()

# Корневой API
#
@app.get("/")
def home_page():
    return {"message": "Hello, world!"}

# API продукта
#
@app.get("/products")
def get_all_products():
    # products = json_to_dict_list(path_to_json_products)
    query = "SELECT * FROM product;"
    products = execute_read_query(connection, query)
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
    print("data--: ",data)
    # print("products--: ",products)
    # получаем пользователя по id (если указан)
    if 'id' in data:
        print("finded 'id' in 'data'")
        print(data["id"])
        # product = find_products(data["id"])
        product = execute_one_record(connection, data["id"])
    else:
        # иначе направляем на создание нового ресурса
        print("Not found index 'id' in 'data'")
        product = None
    print("product--: ",product)
    # если ресурс не найден
    if product == None:
        # если не найден, добавляем новый продукт в список products
        # tmp = Product(data["title"], data["price"], data["quantity"])
        # product = {
        #     # "id": tmp.id,
        #     "title": tmp.title,
        #     "price": tmp.price,
        #     "quantity": tmp.quantity
        # }
        # очищаем память от временной переменной
        # del tmp
        # products.append(product)
        product = execute_input_query(connection, data["title"], data["price"], data["quantity"])
        # record_result = dict_list_to_json(products, path_to_json_products)
        product = {
            "id": product[0],
            "title": product[1],
            "price": product[2],
            "quantity": product[3]
        }
        print("Аdd product: ", product)
        # product = create_product(data)
        return {"message": "PUT запрос выполнен успешно, создан новый продукт", "data": product}
    else:
        # если продукт найден, изменяем его данные и отправляем обратно клиенту
        # index = products.index(product)
        product = execute_update_query(connection, data["title"], data["price"], data["quantity"], data["id"])
        # print("Элемент номер: ", index)
        # products[index]["title"] = data["title"]
        # products[index]["price"] = data["price"]
        # products[index]["quantity"] = data["quantity"]
        # record_result = dict_list_to_json(products, path_to_json_products)
        # print("File update reload: ",record_result,"\n", products,"\n", product)
        print("Update product: ", product)

    return {"message": "PUT запрос выполнен успешно, продукт изменён", "data": data}

@app.delete("/product/{id}")
def delete_product(id):
    product = find_products(id)
    if product == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={ "message": "Продукт не найден" }
        )
    products.remove(product)
    record_result = dict_list_to_json(products, path_to_json_products)
    print("Delete product: ", product)
    return product



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


