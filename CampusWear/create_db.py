import sqlite3

conn = sqlite3.connect("campuswear.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL,
    description TEXT,
    image TEXT
)
""")

conn.commit()

conn.close()

print("Database created successfully.")