import sqlite3

conn = sqlite3.connect("campuswear.db")
cursor = conn.cursor()

cursor.execute("UPDATE products SET stock = 15 WHERE id = 1")
cursor.execute("UPDATE products SET stock = 10 WHERE id = 2")
cursor.execute("UPDATE products SET stock = 20 WHERE id = 3")
cursor.execute("UPDATE products SET stock = 8 WHERE id = 4")

conn.commit()
conn.close()

print("Stock updated successfully!")