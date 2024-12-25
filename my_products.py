import sqlite3
from crud_functions import initiate_db

db_path = "products.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

initiate_db()

products = [
    ("Product1", "Описание продукта 1", 100, "product1.jpg"),
    ("Product2", "Описание продукта 2", 200, "product2.jpg"),
    ("Product3", "Описание продукта 3", 300, "product3.jpg"),
    ("Product4", "Описание продукта 4", 400, "product4.jpg"),
]

cursor.executemany(
    "INSERT INTO Products (title, description, price, image_path) VALUES (?, ?, ?, ?)",
    products
)

connection.commit()
connection.close()

print("Данные успешно добавлены!")