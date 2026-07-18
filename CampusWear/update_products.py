import sqlite3

conn = sqlite3.connect("campuswear.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE products
ADD COLUMN category TEXT
""")

conn.commit()
conn.close()

print("Products table updated!")