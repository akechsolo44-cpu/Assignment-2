import sqlite3

conn = sqlite3.connect("campuswear.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE products
SET category = 'Hoodies'
WHERE name = 'Black Hoodie'
""")

cursor.execute("""
UPDATE products
SET category = 'Jeans'
WHERE name = 'Premium Baggy Jeans'
""")

cursor.execute("""
UPDATE products
SET category = 'T-Shirts'
WHERE name = 'Premium T-Shirt'
""")

cursor.execute("""
UPDATE products
SET category = 'Pants'
WHERE name = 'cargo'
""")

conn.commit()
conn.close()

print("Categories added successfully!")