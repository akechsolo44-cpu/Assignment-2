import sqlite3

conn = sqlite3.connect("campuswear.db")
cursor = conn.cursor()

products = [
    ("Black Hoodie", 35, "Premium cotton hoodie", "hoodie.jpg"),
    ("Baggy Jeans", 40, "Comfortable oversized jeans", "jeans.jpg"),
    ("Campus T-Shirt", 20, "Perfect everyday campus wear", "tshirt.jpg"),
    ("Cargo Pants", 45, "Modern streetwear cargo pants", "cargo.jpg")
]

cursor.executemany("""
INSERT INTO products (name, price, description, image)
VALUES (?, ?, ?, ?)
""", products)

conn.commit()
conn.close()

print("Products added successfully!")