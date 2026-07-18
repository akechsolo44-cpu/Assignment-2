import sqlite3

conn = sqlite3.connect("campuswear.db")
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

cursor.execute("SELECT id, name, stock FROM products")

products = cursor.fetchall()

for product in products:
    print(dict(product))

conn.close()