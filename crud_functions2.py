import sqlite3


def initiate_db():
    connection = sqlite3.connect("product.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL DEFAULT 1000
    )
    """)

    connection.commit()
    connection.close()


def add_user(username, email, age):
    connection = sqlite3.connect("product.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO Users (username, email, age, balance)
    VALUES (?, ?, ?, ? )
    """, (username, email, age, 1000))

    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect("prodact.db")
    cursor = connection.cursor()

    cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()

    connection.close()

    return result is not None
