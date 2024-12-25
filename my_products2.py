import sqlite3
from crud_functions import initiate_db

db_path = "products.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Инициализация базы данных
initiate_db()

# Пример данных для вставки
Users = [
    ("new user", "user@gmail.com", 33, "1000"),
    ("new2user", "user2@gmail.com", 23, "1000"),
    ("new3user", "user3@gmail.com", 26, "1000"),
    ("new4user", "user4@gmail.com", 29, "1000"),
]

# Вставляем данные в таблицу Users (не User)
cursor.executemany(
    "INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
    Users
)

connection.commit()
connection.close()

print("Данные успешно добавлены!")
