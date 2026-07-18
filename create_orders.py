import sqlite3

conn = sqlite3.connect("campuswear.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXIST orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    total REAL
)
""")

conn.commit()
conn.close()

print("Orders table created!")