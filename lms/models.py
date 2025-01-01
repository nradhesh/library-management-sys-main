import sqlite3

#initialised db name
DB_NAME = "library.db"

#initialised db table creation
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            available INTEGER DEFAULT 1
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            borrowed_books TEXT DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()

#book add,deletion,search,borrow
class Book:
    @staticmethod
    def add_book(title, author, isbn):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", (title, author, isbn))
        conn.commit()
        conn.close()

    @staticmethod
    def remove_book(book_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def search_books(keyword):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?", (f'%{keyword}%',) * 3)
        books = cursor.fetchall()
        conn.close()
        return books

    @staticmethod
    def borrow_book(book_id, user_id):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
        available = cursor.fetchone()[0]
        if available:
            cursor.execute("UPDATE books SET available = 0 WHERE id = ?", (book_id,))
            cursor.execute("SELECT borrowed_books FROM users WHERE id = ?", (user_id,))
            borrowed_books = cursor.fetchone()[0]
            new_borrowed = f"{borrowed_books},{book_id}" if borrowed_books else str(book_id)
            cursor.execute("UPDATE users SET borrowed_books = ? WHERE id = ?", (new_borrowed, user_id))
            conn.commit()
        conn.close()

#user add
class User:
    @staticmethod
    def add_user(name):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
