import sqlite3

conn = sqlite3.connect("campuswear.db")
cursor = conn.cursor()

print("TABLES:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

for table in cursor.fetchall():
    print(table[0])

print("\nUSERS")
cursor.execute("SELECT * FROM users")

for row in cursor.fetchall():
    print(row)

print("\nPRODUCTS")
cursor.execute("SELECT * FROM products")

for row in cursor.fetchall():
    print(row)

print("\nORDERS")
cursor.execute("SELECT * FROM orders")

for row in cursor.fetchall():
    print(row)

conn.close()