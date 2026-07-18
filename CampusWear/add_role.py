import sqlite3

conn = sqlite3.connect("campuswear.db")

cursor = conn.cursor()

try:

    cursor.execute("""

        ALTER TABLE users

        ADD COLUMN role TEXT DEFAULT 'customer'

    """)

    print("Role column added successfully!")

except sqlite3.OperationalError:

    print("Role column already exists.")

conn.commit()
conn.close()