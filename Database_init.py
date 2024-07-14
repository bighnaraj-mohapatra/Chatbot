import sqlite3

def init_db():

    # Connect to SQLite database (it will create the database file if it doesn't exist)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create a table to store user credentials
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        contact_number TEXT,
        password TEXT
    )
    ''')

    # Commit and close the connection
    conn.commit()
    conn.close()
