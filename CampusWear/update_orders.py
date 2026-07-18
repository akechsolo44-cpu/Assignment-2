import sqlite3

conn = sqlite3.connect("campuswear.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE orders
ADD COLUMN order_date TEXT
""")

conn.commit()
conn.close()

print("Orders table updated!")