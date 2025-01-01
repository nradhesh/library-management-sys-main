import sqlite3
from datetime import datetime, timedelta

DB_NAME = "library.db"

def check_overdue_books():
    """
    Check for overdue books in the system and generate notifications for users.
    Assumes there is a `borrow_date` column in the `books` table.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Assume books have a borrow date and are due in 14 days
    overdue_days = 14
    overdue_date = datetime.now() - timedelta(days=overdue_days)
    overdue_date_str = overdue_date.strftime("%Y-%m-%d")

    query = """
        SELECT books.id, books.title, users.id AS user_id, users.name
        FROM books
        JOIN users ON ',' || users.borrowed_books || ',' LIKE '%,' || books.id || ',%'
        WHERE books.available = 0 AND books.borrow_date <= ?
    """
    cursor.execute(query, (overdue_date_str,))
    overdue_books = cursor.fetchall()

    for book in overdue_books:
        book_id, book_title, user_id, user_name = book
        print(f"Notification: User '{user_name}' (ID: {user_id}) has an overdue book '{book_title}' (ID: {book_id}).")
    
    conn.close()

def send_notifications():
    """
    Mock function to send notifications to users.
    """
    print("Checking for overdue books...")
    check_overdue_books()
    print("Notifications sent.")

if __name__ == "__main__":
    send_notifications()
