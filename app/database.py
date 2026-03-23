# Подключение к БД PostgreSQL
import psycopg2

def connect():
    try:
        # Подключение к базе
        connection = psycopg2.connect(
            dbname="product_db",
            user="product_owner",
            # user="demyanchenkoao",
            password="1234567890",
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
        # cursor.execute("CREATE TABLE product ( id UUID, title VARCHAR(200) NOT NULL, price NUMERIC, quantity INT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        # cursor.execute("CREATE EXTENSION IF NOT EXISTS 'uuid-ossp';")
        all_tables = cursor.fetchall()
        print(f"Доступны таблицы: {all_tables}")
        # Закрываем соединение
        # cursor.close()
        # connection.close()
        return connection
    except Exception as e:
        print(f"Ошибка подключения: {e}")

# Выполнение SELECT
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        # connection.commit()
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")

# Выполнение SELECT
def execute_one_record(connection, id):
    query = "SELECT * FROM product WHERE id='" + id + "';"
    print(query)
    cursor = connection.cursor()
    result = None
    try:
        # cursor.execute(query)
        cursor.execute(query)
        # connection.commit()
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Select error:'{e}'")

# Выполнение INPUT
def execute_input_query(connection, title, price, quantity):
    query = "INSERT INTO product (title, price, quantity) VALUES (%s,%s,%s) RETURNING id;"
    cursor = connection.cursor()
    result = None
    try:
        # cursor.execute(query)
        cursor.execute(query, (title, price, quantity))
        # connection.commit()
        id_of_new_row = cursor.fetchone()[0]
        result = execute_one_record(connection, id_of_new_row)
        return result
    except Exception as e:
        print(f"Input error '{e}' occurred")

# Выполнение UPDATE
def execute_update_query(connection, title, price, quantity, id):
    query = "UPDATE product SET title=%s, price=%s, quantity=%s WHERE id=%s;"
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, (title, price, quantity, id))
        # connection.commit()
        result = execute_one_record(connection, id)
        return result
    except Exception as e:
        print(f"Update error '{e}' occurred")