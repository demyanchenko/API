# Подключение к БД PostgreSQL
import psycopg2

def connect():
    try:
        # Подключение к базе
        connection = psycopg2.connect(
            dbname="product_db",
            user="product_owner",
            password="1234567890",
            # user="security_owner",
            # password="psecureg109#",
            host="localhost",
            port="5432"
        )
        print("Подключение успешно!")
        connection.autocommit = True
        # Создаём курсор
        cursor = connection.cursor()
        # Выполняем запрос
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"Версия PostgreSQL: {db_version}")
        cursor.execute("SELECT current_database();")
        current_database = cursor.fetchone()
        print(f"Текущая база: {current_database}")
        # Выполняем запрос
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        all_tables = cursor.fetchall()
        print(f"Доступны таблицы: {all_tables}")
        # Закрываем соединение
        cursor.close()
        # connection.close()
        return connection
    except Exception as e:
        print(f"Ошибка подключения: {e}")

# Выполнение SELECT
def db_execute_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        # connection.commit()
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        cursor.close()
        print(f"The error '{e}' occurred")

# Выполнение SELECT by id
def db_select_product_by_id(connection, id):
    query = "SELECT * FROM product WHERE id=%(prod_id)s;"
    print(query)
    cursor = connection.cursor()
    result = None
    try:
        # cursor.execute(query)
        cursor.execute(query, {'prod_id': id,})
        # connection.commit()
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        cursor.close()
        print(f"Select error:'{e}'")

# Выполнение INPUT
def db_input_product(connection, title, price, quantity):
    query = "INSERT INTO product (title, price, quantity) VALUES (%s,%s,%s) RETURNING id;"
    cursor = connection.cursor()
    result = None
    try:
        # cursor.execute(query)
        cursor.execute(query, (title, price, quantity))
        # connection.commit()
        id_of_new_row = cursor.fetchone()[0]
        print(id_of_new_row)
        result = db_select_product_by_id(connection, id_of_new_row)
        print(result)
        # cursor.close()
        return result
    except Exception as e:
        cursor.close()
        print(f"Input error: '{e}'")

# Выполнение UPDATE
def db_update_product_by_id(connection, title, price, quantity, id):
    query = "UPDATE product SET title=%s, price=%s, quantity=%s WHERE id=%s;"
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, (title, price, quantity, id))
        # connection.commit()
        result = db_select_product_by_id(connection, id)
        cursor.close()
        return result
    except Exception as e:
        cursor.close()
        print(f"Update error: '{e}'")

# Выполнение DELETE
def db_delete_product_by_id(connection, id):
    query = "DELETE FROM product WHERE id=%(prod_id)s;"
    print(query, id)
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, {'prod_id': id,})
        # connection.commit()
        # result = execute_one_record(connection, id)
        cursor.close()
        return id
    except Exception as e:
        cursor.close()
        print(f"Delete error: '{e}'")