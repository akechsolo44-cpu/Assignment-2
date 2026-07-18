import sqlite3

conn = sqlite3.connect("campuswear.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE products
ADD COLUMN stock INTEGER
""")

conn.commit()
conn.close()

print("Stock column added successfully!")